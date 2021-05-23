from django.db import models
from django.utils import timezone

from workforce.constants import (PROJECT_STATUS, DESIGNATION, OFFICE,
                    PERCENT_TYPE, WAREHOUSE_CATEGORY, WEATHER_STATUS)

# Create your models here.

BILL_STATUS = (
    ('For Billing','For Billing'),
    ('On-Process', 'On-Process'),
    ('Completed','Completed'),
)

REPORT_TYPE = (
    ('Project Log Sheet','Project Log Sheet'),
    ('Statement of Work Accomplished', 'Statement of Work Accomplished'),
    ('Straight Line Diagram','Straight Line Diagram'),
    ('Geotagged Pictures','Geotagged Pictures'),
    ('Project Monitor','Project Monitor'),
)

ITEM_CATEGORY = (
    ('Facilities for Engineers', 'Facilities for Engineers'),
    ('Other General Requirements', 'Other General Requirements'),
    ('Earth Works', 'Earth Works'),
    ('Sub Base and Base Course', 'Sub Base and Base Course'),
    ('Surface Course', 'Surface Course'),
    ('Drainage and Slope Protection', 'Drainage and Slope Protection'),
    ('Miscellaneous', 'Miscellaneous'),
    ('Bridge Construction','Bridge Construction'),
    ('Water Supply','Water Supply')
)

EXPENSE_CATEGORY = (
    ('Cement', 'Cement'),
    ('Labor', 'Labor'),
    ('Fuel', 'Fuel'),
    ('General & Admin','General & Admin'),
    ('Materials', 'Materials'),
    ('Overhead', 'Overhead'),
    ('Equipment', 'Equipment'),
)

LICENSE_USED = (
    ('AIP', 'AIP'),
    ('BMK', 'BMK'),
    ('BMK/AIP', 'BMK/AIP'),
)

IMPLEMENTING_OFFICE = (
    ('DPWH-CAR', 'DPWH-CAR'),
    ('DPWH-REGION I', 'DPWH-REGION I'),
    ('DPWH-REGION II', 'DPWH-REGION II'),
    ('DPWH-MPFDEO', 'DPWH-MPFDEO'),
    ('DPWH-BFDEO', 'DPWH-BFDEO'),
    ('DPWH-IS2DEO', 'DPWH-IS2DEO'),
    ('LGU-SAN EMILIO', 'LGU-SAN EMILIO'),
    ('LGU-BONTOC', 'LGU-BONTOC'),
    ('ALTERNERGY', 'ALTERNERGY'),
)

class Project(models.Model):
    project_code = models.CharField('Project Code', max_length=40)
    project_name = models.CharField('Project Name', max_length=200)
    project_detail = models.TextField('Contract Name')
    project_status = models.CharField('Status', max_length=200, default='Under Construction', choices=PROJECT_STATUS)
    project_pic = models.ImageField('Project Profile', upload_to='project_pic', default='profile_pic/default.png')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.project_code)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

class Detail(models.Model):
    base_project = models.OneToOneField('operation.Project', related_name='detail', on_delete = models.CASCADE)
    license = models.CharField('License', max_length=200, choices=LICENSE_USED)
    project_id = models.CharField('Project ID', max_length=200)
    implementing_office = models.CharField('Implementing Office', max_length=200, choices=IMPLEMENTING_OFFICE)
    award_date = models.DateField('Notice of Award Date', default=timezone.now)
    proceed_date = models.DateField('Notice to Proceed Date', default=timezone.now)
    effectivity_date = models.DateField('Effectivity Date', default=timezone.now)
    expiry_date = models.DateField('Expiry Date', default=timezone.now)
    time_extension = models.DecimalField('Time Extension (Days)', max_digits=20, decimal_places=0, default=0)
    contract_duration = models.DecimalField('Contract Duration', max_digits=20, decimal_places=0, default=0)
    contract_cost = models.DecimalField('Contract Cost', max_digits=20, decimal_places=2, default=0)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.base_project)

    class Meta:
        verbose_name = 'Project Detail'
        verbose_name_plural = 'Project Details'


class Personnel(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='personnel', on_delete = models.CASCADE)
    office = models.CharField('Specifics', max_length=200, choices=OFFICE)
    title = models.CharField('Title', max_length=200, choices=DESIGNATION)
    name = models.CharField('Name', max_length=200)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = 'Personnel'
        verbose_name_plural = 'Personnel'


class WorkStat(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='work', on_delete = models.CASCADE)
    date = models.DateField('Date', blank=True, null=True)
    planned = models.DecimalField('Planned Value', max_digits=20, decimal_places=3, blank=True, null=True)
    actual = models.DecimalField('Actual Value', max_digits=20, decimal_places=3, blank=True, null=True)
    slippage = models.DecimalField('Slippage', max_digits=20, decimal_places=3, blank=True, null=True)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.base_project)

    class Meta:
        verbose_name = 'Work Stat'
        verbose_name_plural = 'Work Stat'


class AllocatedExpense(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='allocated_expense', on_delete = models.CASCADE, null=True)
    date = models.DateField('Date', blank=True, null=True)
    materials = models.DecimalField('Materials', max_digits=20, decimal_places=2, default=0)
    equipment = models.DecimalField('Equipment', max_digits=20, decimal_places=2, default=0)
    labor = models.DecimalField('Labor', max_digits=20, decimal_places=2, default=0)
    overhead = models.DecimalField('Overhead', max_digits=20, decimal_places=2, default=0)
    admin = models.DecimalField('Admin', max_digits=20, decimal_places=2, default=0)
    drawings = models.DecimalField('Drawings', max_digits=20, decimal_places=2, default=0)
    vat = models.DecimalField('VAT', max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=20, decimal_places=2, default=0)
    document = models.FileField('Document', upload_to='major_expense/', default=' ')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.base_project)

    class Meta:
        verbose_name = 'Allocated Expense'
        verbose_name_plural = 'Allocated Expense'
        get_latest_by = 'date'


class MajorExpense(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='major_expense', on_delete = models.CASCADE, null=True)
    date = models.DateField('Date', blank=True, null=True)
    materials = models.DecimalField('Materials', max_digits=20, decimal_places=2, default=0)
    equipment = models.DecimalField('Equipment', max_digits=20, decimal_places=2, default=0)
    labor = models.DecimalField('Labor', max_digits=20, decimal_places=2, default=0)
    overhead = models.DecimalField('Overhead', max_digits=20, decimal_places=2, default=0)
    admin = models.DecimalField('Admin', max_digits=20, decimal_places=2, default=0)
    drawings = models.DecimalField('Drawings', max_digits=20, decimal_places=2, default=0)
    vat = models.DecimalField('VAT', max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=20, decimal_places=2, default=0)
    document = models.FileField('Document', upload_to='major_expense/', default=' ')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.base_project)

    class Meta:
        verbose_name = 'Actual Expense'
        verbose_name_plural = 'Actual Expense'
        get_latest_by = 'date'



class Item(models.Model):
    item_no = models.CharField('Item No', max_length=200)
    category = models.CharField('Category', max_length=200, choices=ITEM_CATEGORY)
    description = models.CharField('Item Description', max_length=200)

    def __str__(self):
        return "%s" %(self.description)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class ProjectItem(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='project_item', on_delete = models.CASCADE)
    item = models.ForeignKey('operation.Item', related_name='item', on_delete = models.CASCADE)
    start_date = models.DateField('_____Date of Start_____', default=timezone.now)
    end_date = models.DateField('_____Date of End_____', default=timezone.now)
    sequence = models.DecimalField('Sequence', max_digits=20, decimal_places=0, default=0)
    dependency = models.DecimalField('Dependency', max_digits=20, decimal_places=0, blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=3, default=0)
    planned_work = models.DecimalField('Weighted %', max_digits=20, decimal_places=3, default=0)
    actual_work = models.DecimalField('Work Done (%)', max_digits=20, decimal_places=3, default=0)


    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.item)

    class Meta:
        verbose_name = 'Project Item'
        verbose_name_plural = 'Project Items'


class Report(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='op_status', on_delete = models.CASCADE)
    date = models.DateField('Date', default=timezone.now)
    activity = models.TextField('Activity Details')
    issues = models.TextField('Issues')
    weather = models.CharField('Weather Condition', max_length=200, default='Sunny', choices=WEATHER_STATUS)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.date)

    class Meta:
        verbose_name = 'Daily Report'
        verbose_name_plural = 'Daily Reports'
        get_latest_by = 'date'

class Gallery(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='gallery', on_delete = models.CASCADE)
    date = models.DateField('Date', default=timezone.now)
    title = models.CharField('Title', max_length=200)
    detail = models.TextField('Details', default='Details here...')

    def __str__(self):
        return "%s" %(self.date)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'
        ordering = ['-date',]

class Slides(models.Model):
    base_gallery = models.ForeignKey('operation.Gallery', related_name='gallery_slides', on_delete = models.CASCADE)
    date = models.DateField('Date', default=timezone.now)
    title = models.CharField('Title', max_length=200)
    detail = models.CharField('Details', max_length=500)
    image = models.ImageField('Project Profile', upload_to='project_images', blank=True, default=' ')

    def __str__(self):
        return "%s" %(self.date)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'
        ordering = ['-date',]


class Billing(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='billing', on_delete = models.CASCADE)
    title = models.CharField('Title', max_length=200)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)
    status = models.CharField('Status', max_length=200, choices=BILL_STATUS)
    date = models.DateField('Date Deposited', default=timezone.now)
    document = models.FileField('Billing Document', upload_to='billing_docs/', blank=True, null=True)
    image = models.ImageField('Cheque', upload_to='billing_checks', default='profile_pic/default.png')

    def __str__(self):
        return "%s" %(self.base_project)

    class Meta:
        verbose_name = 'Billing'
        verbose_name_plural = 'Billings'
        ordering = ['-date',]


class Reporting(models.Model):
    base_project = models.ForeignKey('operation.Project', related_name='reports', on_delete = models.CASCADE)
    date = models.DateField('Date', default=timezone.now)
    report_type = models.CharField('Type', max_length=200, choices=REPORT_TYPE)
    remarks = models.CharField('Remarks', max_length=200, default='', blank=True)
    document = models.FileField('Upload Report', upload_to='reports_docs/')

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.base_project)

    class Meta:
        verbose_name = 'Scheduled Report'
        verbose_name_plural = 'Scheduled Reports'
        ordering = ['-date',]



