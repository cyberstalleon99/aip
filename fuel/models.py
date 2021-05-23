from django.db import models
from django.utils import timezone

from workforce.models import BasicProfile, ProjectSite
from fleet.models import UnitProfile

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


#Validators
def validate_upload_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('Warning file size is more than 1MB'),params={'value': value},)


TYPE = (
    ('Incoming','Incoming'),
    ('Outgoing','Outgoing'),
    ('Transfer','Transfer'),
)

# Create your models here.
class Transaction(models.Model):
    trans_date = models.DateTimeField('Date', default=timezone.now)
    trans_type = models.CharField('Transaction', max_length=200, choices=TYPE)
    fwf = models.CharField('FWF No.', max_length=50, default=0)
    processed_by = models.ForeignKey(BasicProfile, related_name='processed_by', null=True, on_delete = models.SET_NULL)
    tank_site = models.ForeignKey('fuel.Tank', related_name='trans_tank_site', null=True, on_delete = models.SET_NULL)
    project_site = models.ForeignKey(ProjectSite, related_name='trans_project_site', null=True, on_delete = models.SET_NULL)
    unit = models.ForeignKey(UnitProfile, related_name='trans_unit', null=True, on_delete = models.SET_NULL)
    amount = models.DecimalField('Amount/Liters', max_digits=20, decimal_places=2, default=0)
    price = models.DecimalField('Unit Price', max_digits=20, decimal_places=2, default=0)
    attachment = models.ImageField('Attach Form', upload_to='fuel_forms', validators=[validate_upload_size])
    remarks = models.TextField('Remarks', blank=True, null=True)

    smr = models.DecimalField('SMR', max_digits=20, decimal_places=2, default=0)
    kmr = models.DecimalField('KMR', max_digits=20, decimal_places=2, default=0)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.unit)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

class Tank(models.Model):
    name = models.CharField('Name', max_length=200)
    location = models.ForeignKey(ProjectSite, related_name='tank_site', null=True, on_delete = models.SET_NULL)
    max_capacity = models.DecimalField('Maximum Capacity/Liters', max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = 'Tank'
        verbose_name_plural = 'Tanks'

class Reading(models.Model):
    tank = models.ForeignKey('fuel.Tank', related_name='tank', on_delete = models.CASCADE)
    read_date = models.DateTimeField('Date', default=timezone.now)
    conducted_by = models.ForeignKey(BasicProfile, related_name='read_by', null=True, on_delete = models.SET_NULL)
    reading = models.DecimalField('Amount/Liters', max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return "%s" %(self.tank)

    class Meta:
        verbose_name = 'Reading'
        verbose_name_plural = 'Readings'
