from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from workforce.models import ProjectSite, Outsider
from accounting.models import Item
from fleet.models import UnitProfile
from workforce.constants import OUTGOING_TYPE, WORK_ITEM

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#Validators
def validate_upload_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('Warning file size is more than 1MB'),params={'value': value},)


VERIFICATION = (
    ('For Verification', 'For Verification'),
    ('Verified', 'Verified'),
)

def user_unicode_patch(self):
    return '%s %s' % (self.first_name, self.last_name)

User.__str__ = lambda user: user.get_full_name() or user.get_username()

class Incoming(models.Model):
    trans_date = models.DateTimeField('Date', db_index=True, default=timezone.now)
    received_by = models.ForeignKey(User, related_name='in_received_by', default=32, on_delete = models.SET_NULL, null=True)
    form_no = models.CharField('FORM No', db_index=True, max_length=20, default=0)
    trans_no = models.CharField('Tracking No', db_index=True, max_length=20, default=0)
    project_site = models.ForeignKey(ProjectSite, related_name='in_project_site', default=7, null=True, on_delete = models.SET_NULL)
    item = models.ForeignKey(Item, related_name='item_in', null=True, on_delete = models.SET_NULL)
    quantity = models.DecimalField('Quantity', db_index=True, max_digits=20, decimal_places=2, default=0)
    details = models.TextField('Details', default='Details here...')
    attachment = models.FileField('Form', upload_to='incoming_form', blank=True, validators=[validate_upload_size])
    unit_price = models.DecimalField('Unit Price', max_digits=20, decimal_places=2, default=0)
    status = models.CharField('Status', max_length=200, default='For Verification', choices=VERIFICATION)

    create_date = models.DateTimeField('Date Created', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='incoming_created_by')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='incoming_modified_by')

    def __str__(self):
        return "%s" %(self.id)

    class Meta:
        verbose_name = 'Incoming'
        verbose_name_plural = 'Incomings'

class Outgoing(models.Model):
    base_in = models.ForeignKey('warehouse.Incoming', related_name='out', on_delete = models.SET_NULL, null=True)
    trans_date = models.DateField('Date', default=timezone.now)
    trans_type = models.CharField('Type', max_length=50, choices = OUTGOING_TYPE)
    form_no = models.CharField('FORM No', max_length=20, default=0)
    project_site = models.ForeignKey(ProjectSite, related_name='out_project_site', null=True, on_delete = models.SET_NULL)
    released_by = models.ForeignKey(User, related_name='out_released_by', default='', on_delete = models.SET_NULL, null=True)
    released_to = models.ForeignKey(User, related_name='out_released_to', blank=True, null=True, on_delete = models.SET_NULL)
    released_out = models.ForeignKey(Outsider, related_name='outsider_released_to', blank=True, null=True, on_delete = models.SET_NULL)
    unit = models.ForeignKey(UnitProfile, related_name='user_unit', blank=True, null=True, on_delete = models.SET_NULL)

    quantity = models.DecimalField('Quantity', db_index=True, max_digits=20, decimal_places=2, default=0)
    details = models.CharField('Details', max_length=200, default='')
    attachment = models.FileField('Form', upload_to='incoming_form', blank=True, validators=[validate_upload_size])
    status = models.CharField('Status', max_length=200, default='For Verification', choices=VERIFICATION)

    item_work = models.CharField('Work Item', max_length=200, default='N/A', choices=WORK_ITEM)

    create_date = models.DateTimeField('Date Created', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='outgoing_created_by')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='outgoing_modified_by')

    def __str__(self):
        return "%s" %(self.trans_date)

    class Meta:
        verbose_name = 'Outgoing'
        verbose_name_plural = 'Outgoings'




