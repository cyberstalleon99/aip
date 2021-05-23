import os
from django.db import models
from django.utils import timezone
from datetime import date
from django.core.mail import send_mail

from workforce.models import BasicProfile, ProjectSite
from accounting.models import Item


from workforce.constants import (STATUS, STATUS_REPAIR,
            SERVICE_TYPE, REPAIR_CAUSE, UNIT_TYPE, UNIT_ATTACH, FILE_STAT,
            DELIVERY_STAT, TYPE_AGGREGATE, STATUS_TRAVEL)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from twilio.rest import Client

TRIP_TYPE = (
    ('One Way', 'One Way (Mabayag nga agsubli)'),
    ('Two Way', 'Two Way (Balikan)')
)

#Validators
def validate_upload_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('Warning file size is more than 1MB'),params={'value': value},)


# Create your models here.
class UnitProfile(models.Model):
    body_no = models.CharField('Body No', max_length=200)
    plate_no = models.CharField('Plate No', max_length=200, default='No Plate')
    unit_type = models.CharField('Unit Type', max_length=200, choices=UNIT_TYPE, default='Uncategorized')
    unit_desc = models.CharField('Unit Description', max_length=500)
    operator = models.ForeignKey(BasicProfile, related_name='operator', null=True, on_delete = models.SET_NULL)
    project_site = models.ForeignKey(ProjectSite, related_name='project_site', null=True, on_delete = models.SET_NULL)
    status = models.CharField('Status', max_length=200, choices=STATUS)
    profile_pic = models.ImageField('Unit Pic', upload_to='unit_pic', default='profile_pic/default.png')
    model = models.CharField('Model', max_length=200, blank=True, null=True)
    engine_no = models.CharField('Engine No', max_length=200, default=0)
    chassis_no = models.CharField('Chassis No', max_length=200, default=0)
    net_capacity = models.DecimalField('Net Capacity.', max_digits=20, decimal_places=0, default=0)
    fuel_capacity = models.DecimalField('Fuel Capacity.', max_digits=20, decimal_places=0, default=0)
    registered_owner = models.ForeignKey(BasicProfile, related_name='owner', null=True, on_delete = models.SET_NULL)
    price = models.DecimalField('Price', max_digits=20, decimal_places=0, default=0)
    cr = models.CharField('CR', max_length=200, blank=True, null=True)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.body_no)

    class Meta:
        verbose_name = 'Unit Profile'
        verbose_name_plural = 'Unit Profile'


class Operator(models.Model):
    base_unit = models.ForeignKey('fleet.UnitProfile', related_name='op_history', null=True, on_delete = models.SET_NULL)
    operator = models.ForeignKey(BasicProfile, related_name='unit_operator', null=True, on_delete = models.SET_NULL)
    date_start = models.DateField('From', default=timezone.now)
    date_end = models.DateField('To', default=timezone.now)

    def __str__(self):
        return "%s" %(self.base_unit)

    class Meta:
        verbose_name = 'Operator'
        verbose_name_plural = 'Operators'


class Travel(models.Model):
    base_unit = models.ForeignKey('fleet.UnitProfile', related_name='travel_history', null=True, on_delete = models.SET_NULL)
    requested_by = models.ForeignKey(BasicProfile, blank=True, null=True, on_delete = models.SET_NULL)
    driver = models.ForeignKey(BasicProfile, related_name='travel_operator', null=True, on_delete = models.SET_NULL)
    date_start = models.DateField('Date of Travel', default=timezone.now)
    source = models.ForeignKey(ProjectSite, related_name='travel_source', null=True, blank=True, on_delete = models.SET_NULL)
    destination = models.ForeignKey(ProjectSite, related_name='travel_dest', null=True, blank=True, on_delete = models.SET_NULL)
    note = models.TextField('Details',)
    status = models.CharField('Status', max_length=50, null=True, blank=True, default='For Approval', choices=STATUS_TRAVEL)
    trip = models.CharField('Trip', max_length=50, choices=TRIP_TYPE)

    create_date = models.DateTimeField('Date Created', auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    returning_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s" %(self.base_unit)

    def get_route(self):
        return f"{self.source} - {self.destination}"

    class Meta:
        verbose_name = 'Travel'
        verbose_name_plural = 'Travel'


class Tools(models.Model):
    base_unit = models.ForeignKey('fleet.UnitProfile', related_name='tools_attached', null=True, on_delete = models.SET_NULL)
    item = models.ForeignKey(Item, related_name='unit_tools', null=True, on_delete = models.SET_NULL)
    quantity = models.DecimalField('Quantity', max_digits=20, decimal_places=2, default=0)
    remarks = models.CharField('Remarks', max_length=200, default='Notes here')

    def __str__(self):
        return "%s" %(self.item)

    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'


class JobOrder(models.Model):
    base_unit = models.ForeignKey('fleet.UnitProfile', related_name='repair_unit', null=True, on_delete = models.SET_NULL)
    jo_no = models.CharField('JO No.', max_length=200, default='None')
    request_date = models.DateTimeField('Request Date', default=timezone.now)
    site = models.ForeignKey(ProjectSite, related_name='jo_location', null=True, on_delete = models.SET_NULL)
    request_by = models.ForeignKey(BasicProfile, related_name='request_by', null=True, on_delete = models.SET_NULL)
    smr = models.DecimalField('SMR', max_digits=20, decimal_places=2, default=0)
    kmr = models.DecimalField('KMR', max_digits=20, decimal_places=2, default=0)
    detail = models.TextField('Job Request Details')
    status = models.CharField('Status', max_length=200, choices=STATUS_REPAIR, default='For Approval')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.jo_no)

    class Meta:
        verbose_name = 'Job Order Request'
        verbose_name_plural = 'Job Order Request'


class JOImage(models.Model):
    base_profile = models.ForeignKey('fleet.JobOrder', related_name='jo_images', on_delete = models.CASCADE)
    description = models.CharField('Description', max_length=200)
    jo_pic = models.ImageField('Image', upload_to='jo_pic', blank=True, validators=[validate_upload_size])

    def __str__(self):
        return "%s" %(self.base_profile)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Manpower(models.Model):
    base_wo = models.ForeignKey('fleet.WorkOrder', related_name='manpower', on_delete = models.CASCADE)
    crew = models.ForeignKey(BasicProfile, related_name='manpower', null=True, on_delete = models.SET_NULL)
    remarks = models.CharField('Details of Work Done', max_length=200)

    def __str__(self):
        return "%s" %(self.crew)

    class Meta:
        verbose_name = 'Manpower'
        verbose_name_plural = 'Manpower'


class WorkOrder(models.Model):
    base_jo = models.ForeignKey('fleet.JobOrder', related_name='work_order', on_delete = models.CASCADE)
    date_start = models.DateTimeField('Date Started', default=timezone.now)
    date_end = models.DateTimeField('Est. Date of Accomplishment', default=timezone.now)
    service_type = models.CharField('Type of Service', max_length=200, choices=SERVICE_TYPE)
    repair_cause = models.CharField('Cause of Repair', max_length=200, choices=REPAIR_CAUSE)
    scope_work = models.TextField('Scope of Work', default='Enter the scope of work to be done')
    work_done = models.TextField('Details of Work Done')
    remarks = models.TextField('Remarks')
    wo_status = models.CharField('Status', max_length=200, choices=STATUS_REPAIR, default='Under Repair')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    @property
    def running_days(self):
        return (timezone.now()-self.date_start).days

    def __str__(self):
        return "%s" %(self.base_jo)

    class Meta:
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'


class UtilizationReport(models.Model):
    date = models.DateField('Date', default=timezone.now)
    employee_id = models.CharField('ID No.', max_length=40)
    unit_id = models.CharField('Body No', max_length=50)
    smr_start = models.DecimalField('SMR Start', max_digits=20, decimal_places=2, default=0)
    smr_end = models.DecimalField('SMR End', max_digits=20, decimal_places=2, default=0)
    kmr_start = models.DecimalField('KMR Start', max_digits=20, decimal_places=2, default=0)
    kmr_end = models.DecimalField('KMR End', max_digits=20, decimal_places=2, default=0)
    remarks = models.TextField('Remarks', blank=True)
    project_site = models.CharField('Project Site', max_length=100)
    start_hour = models.CharField('Start', max_length=50)
    end_hour = models.CharField('End', max_length=50)
    twh = models.DecimalField('TWH', max_digits=20, decimal_places=2, default=0)
    activity = models.CharField('Activity', max_length=40)
    material = models.CharField('Material', max_length=40, blank=True)
    load = models.DecimalField('Load', max_digits=10, decimal_places=2, default=0)
    operator = models.CharField('Operator', max_length=40)
    unit_type = models.CharField('Unit Type', max_length=50)

    def __str__(self):
        return "%s" %(self.date)

    class Meta:
        verbose_name = 'Utilization Report'
        verbose_name_plural = 'Utilization Reports'


class Attachment(models.Model):
    base_profile = models.ForeignKey('fleet.UnitProfile', related_name='unit_files', on_delete = models.CASCADE)
    document_type = models.CharField('Document Type', max_length=200, choices=UNIT_ATTACH)
    issued_date = models.DateField('Date Issued', default=timezone.now)
    expiry_date = models.DateField('Expiry Date', default=timezone.now)
    doc_file = models.FileField('Document', upload_to='unit_files', blank=True,  default='')
    status = models.CharField('Status', max_length=50, default='', choices=FILE_STAT)
    remarks = models.CharField('Remarks', max_length=200, default='')

    def days2expiry(self):
        return (self.expiry_date - date.today()).days +1

    def __str__(self):
        return "%s" %(self.document_type)

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'


class Slides(models.Model):
    base_profile = models.ForeignKey('fleet.UnitProfile', related_name='unit_images', on_delete = models.CASCADE)
    description = models.CharField('Description', max_length=200)
    slide_pic = models.ImageField('Image', upload_to='unit_pic', blank=True, validators=[validate_upload_size])

    def __str__(self):
        return "%s" %(self.base_profile)

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'



class Delivery(models.Model):
    request_by = models.ForeignKey(BasicProfile, related_name='delivery_request_by', null=True, on_delete = models.SET_NULL)
    source = models.ForeignKey(ProjectSite, related_name='delivery_source', null=True, on_delete = models.SET_NULL)
    destination = models.ForeignKey(ProjectSite, related_name='delivery_destination', null=True, on_delete = models.SET_NULL)
    description = models.CharField('Description', max_length=100)
    status = models.CharField('Status', max_length=50, default='For Pick-Up', choices=DELIVERY_STAT)
    remarks = models.TextField('Details')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            subject = 'AIP Padala: ' + str(self.description)
            message = 'A delivery has been filed! Link: https://eakdev.pythonanywhere.com/fleet/padala/'
            send_mail(
                subject,
                message,
                'aip911dispatch@gmail.com',
                ['aip911dispatch@gmail.com',],
                fail_silently=False,
            )
        super(Delivery, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" %(self.request_by)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
















