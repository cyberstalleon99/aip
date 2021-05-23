from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from workforce.models import ProjectSite, BasicProfile, Subcon
from workforce.constants import (ITEM_CATEGORY, ORDER_STATUS)

LIQUIDATION_TYPE = (
    ('Expense','Expense'),
    ('Excess', 'Excess'),
)

ACCOUNT_CATEGORY = (
    ('Uncategorized','Uncategorized'),
    ('Materials', 'Materials'),
    ('Labor','Labor'),
    ('General & Admin','General & Admin'),
    ('Overhead','Overhead'),
)
DEBIT_CREDIT = (
    ('Debit','Debit'),
    ('Adjustment','Adjustment'),
    ('Credit', 'Credit'),
)
PAYMENT_MODE = (
    ('Cash','Cash'),
    ('Credit','Credit'),
)
CF_STATUS = (
    ('Unliquidated', 'Unliquidated'),
    ('For Review','For Review'),
    ('Verified', 'Verified'),
)

CASH_TRANS_TYPE = (
    ('Cash In','Cash In'),
    ('Cash Out','Cash Out'),
)

ENTRY_TYPE = (
    ('Non-Cash','Non-Cash'),
    ('Receipts','Receipts'),
    ('Disbursements','Disbursements'),
)

ENTRY_STATUS = (
    ('N/A', 'N/A'),
    ('Unliquidated','Unliquidated'),
    ('Liquidated', 'Liquidated'),
)

BILLING_STATUS = (
    ('Open', 'Open'),
    ('For-Review','For-Reveiw'),
    ('Closed', 'Closed'),
)


#Validators
def validate_upload_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('Warning file size is more than 1MB'),params={'value': value},)


def user_unicode_patch(self):
    return '%s %s' % (self.first_name, self.last_name)

User.__str__ = lambda user: user.get_full_name() or user.get_username()


class Item(models.Model):
    item_name = models.CharField('Name', db_index=True, max_length=200)
    general_name = models.CharField('Class Name', max_length=200)
    item_category = models.CharField('Category', max_length=200, choices=ITEM_CATEGORY)
    item_unit = models.CharField('Unit', max_length=200)
    item_detail = models.TextField('Detail')

    def __str__(self):
        return "%s" %(self.item_name)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class Supplier(models.Model):
    name = models.CharField('Name', db_index=True, max_length=200)
    tin = models.CharField('TIN', max_length=200)
    address = models.CharField('Address', max_length=200)
    contact = models.CharField('Contact', max_length=200)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class PriceList(models.Model):
    item = models.ForeignKey('accounting.Item', related_name='item_pl', on_delete = models.SET_NULL, null=True)
    supplier = models.ForeignKey('accounting.Supplier', related_name='supplier_pl', on_delete = models.SET_NULL, null=True)
    price = models.DecimalField('Price', max_digits=20, decimal_places=2, default=0)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s" %(self.item)

    class Meta:
        verbose_name = 'Price List'
        verbose_name_plural = 'Price List'


class ItemCode(models.Model):
    item_code = models.CharField('Code', max_length=10)
    sc1 = models.CharField('General Ledger Account', max_length=200, default='')
    sc2 = models.CharField('Subsidiary Ledger Account 1', max_length=200, default='', blank=True)
    sc3 = models.CharField('Subsidiary Ledger Account 2', max_length=200, default='', blank=True)

    def __str__(self):
        return "%s - %s %s %s" %(self.item_code, self.sc1, self.sc2, self.sc3)

    class Meta:
        verbose_name = 'Chart of Account'
        verbose_name_plural = 'Chart of Accounts'


# for POR
class OrderRequest(models.Model):
    request_date = models.DateTimeField('Date', default=timezone.now)
    request_form = models.CharField('POR No', max_length=50, default=0)
    request_by = models.ForeignKey(User, related_name='or_by', null=True, on_delete = models.SET_NULL)
    project_site = models.ForeignKey(ProjectSite, related_name='or_project_site', null=True, on_delete = models.SET_NULL)

    item = models.ForeignKey('accounting.Item', related_name='item_request', null=True, on_delete = models.SET_NULL)
    quantity = models.DecimalField('Quantity', max_digits=20, decimal_places=2, default=0)
    details = models.TextField('Details', default='Details here...')
    jo_no = models.CharField('JO No', max_length=20, blank=True, null=True)
    form_attach = models.ImageField('Image', upload_to='po_forms', blank=True, validators=[validate_upload_size])

    today = models.BooleanField('Today?', default=False)
    purchaser = models.ForeignKey(User, related_name='purchased_by', blank=True, on_delete = models.SET_NULL, null=True)
    status = models.CharField('Status', max_length=200, default='For Approval', choices=ORDER_STATUS)

    create_date = models.DateTimeField('Date Created', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='por_created_by')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='por_modified_by')


    def save(self, *args, **kwargs):
        if not self.id:
            if self.item.item_category == 'Construction Materials':
                subject = 'PO Request: ' + str(self.item)
                message = 'A Purchase Request has been filed! Link: https://eakdev.pythonanywhere.com/accounting/pending/'
                send_mail(
                    subject,
                    message,
                    'aip911dispatch@gmail.com',
                    ['mayannduran.aip@gmail.com',],
                    fail_silently=False,
                )
        super(OrderRequest, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" %(self.id)

    class Meta:
        verbose_name = 'Item Request'
        verbose_name_plural = 'Item Request'


#This is the latest liquidations
class Entry(models.Model):
    #general fields
    trans_date = models.DateField('Transaction Date (Actual):', default=timezone.now)
    form_no = models.CharField('Form No.', max_length=50)
    base_por = models.ForeignKey('accounting.OrderRequest', verbose_name='POR Trans #',related_name='entry_por', blank=True, null=True, on_delete = models.SET_NULL)
    transaction_by = models.ForeignKey(User, related_name='trans_by', on_delete = models.SET_NULL, blank=True, null=True)
    project_site = models.ForeignKey(ProjectSite, related_name='entry_project_site', on_delete = models.SET_NULL, null=True)
    debit = models.DecimalField('Debit', max_digits=20, decimal_places=2, default=0)
    #credit = models.DecimalField('Credit', max_digits=20, decimal_places=2, default=0)
    remarks = models.TextField('Remarks', blank=True)

    #liquidation fields
    item = models.ForeignKey('accounting.Item', related_name='entry_item', null=True, blank=True, on_delete = models.SET_NULL)
    quantity = models.DecimalField('Quantity', max_digits=20, decimal_places=2, default=0)
    supplier = models.ForeignKey('accounting.Supplier', related_name='entry_supplier', blank=True, null=True, on_delete = models.SET_NULL)
    utang = models.BooleanField('Credit?', default=False)

    #accounting fields
    account_code = models.ForeignKey('accounting.ItemCode', related_name='account_code', blank=True, on_delete = models.SET_NULL, null=True)
    entry_type = models.CharField('Type', max_length=50, choices=ENTRY_TYPE, default='Non-Cash')
    subcon = models.ForeignKey(Subcon, related_name='subcon', blank=True, on_delete = models.SET_NULL, null=True)
    status = models.CharField('Status', max_length=200, choices=ENTRY_STATUS, default='N/A')
    attachment = models.FileField('Attachment', upload_to='entry_files', blank=True, default="")
    entry_debit = models.BooleanField('Debit?', default=False)
    entry_credit = models.BooleanField('Credit?', default=False)

    vat = models.BooleanField('Vatable?', default=False)
    incoming_vat = models.DecimalField('Vat', max_digits=20, decimal_places=2, default=0, editable=False)
    vatable_sales = models.DecimalField('Vatable Sales', max_digits=20, decimal_places=2, editable=False)


    #monitoring
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='entry_created_by')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='entry_modified_by')

    def save(self, *args, **kwargs):
        if self.vat is True:
            self.incoming_vat = (self.debit/Decimal('1.12').quantize(Decimal('1.00')))*Decimal('.12').quantize(Decimal('1.00'))
            self.vatable_sales = self.debit - self.incoming_vat
        else:
            self.vatable_sales = self.debit
            self.incoming_vat = 0
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" %(self.id)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'


class FundRequest(models.Model):
    trans_date = models.DateField('Transaction Date (Actual):', default=timezone.now)
    request_to = models.ForeignKey(User, related_name='request_to', on_delete = models.SET_NULL, null=True)
    project_site = models.ForeignKey(ProjectSite, related_name='request_project_site', on_delete = models.SET_NULL, null=True)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)
    remarks = models.TextField('Remarks')

    done = models.BooleanField(default=False)

    #monitoring
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='request_created_by')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='request_modified_by')


    def __str__(self):
        return "%s" %(self.id)

    class Meta:
        verbose_name = 'Fund Request'
        verbose_name_plural = 'Fund Requests'


class SubconBilling(models.Model):
    trans_date = models.DateField('Transaction Date (Actual):', default=timezone.now)
    request_by = models.ForeignKey(User, related_name='bill_request_by', on_delete = models.SET_NULL, null=True)
    project_site = models.ForeignKey(ProjectSite, related_name='bill_project_site', on_delete = models.SET_NULL, null=True)
    subcon = models.ForeignKey(Subcon, related_name='bill_subcon', on_delete = models.SET_NULL, null=True)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)

    #Operations
    status_ops = models.CharField('Status', max_length=200, choices=BILLING_STATUS, default='Open')
    file_ops = models.FileField('Attachment', upload_to='billing_files', blank=True, default="")
    remarks_ops = models.TextField('Remarks', blank=True)

    #Accounting
    status_acc = models.CharField('Status', max_length=200, choices=BILLING_STATUS, default='Open')
    file_acc = models.FileField('Attachment', upload_to='billing_files', blank=True, default="")
    remarks_acc = models.TextField('Remarks', blank=True)

    #Warehouse
    status_wh = models.CharField('Status', max_length=200, choices=BILLING_STATUS, default='Open')
    file_wh = models.FileField('Attachment', upload_to='billing_files', blank=True, default="")
    remarks_wh = models.TextField('Remarks', blank=True)

    #monitoring
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='billing_created_by')
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='billing_modified_by')

    def __str__(self):
        return "%s" %(self.id)

    class Meta:
        verbose_name = 'Subcon Billing'
        verbose_name_plural = 'Subcon Billings'










#Old Ones
class CashBudget(models.Model):
    trans_type = models.CharField('Transaction', max_length=200, default='Cash Out', choices=CASH_TRANS_TYPE)
    trans_date = models.DateField('Transaction Date:', default=timezone.now)
    form_no = models.CharField('Form No.', max_length=20)
    issued_by = models.ForeignKey(User, related_name='cs_issued_by', on_delete = models.SET_NULL, null=True)
    issued_to = models.ForeignKey(User, related_name='cs_issued_to', on_delete = models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)
    detail = models.CharField('Detail', max_length=200)
    doc_file = models.FileField('Form', upload_to='cf_files', blank=True, default="")

    cdv_date = models.DateField('CDV Date:', default=timezone.now)
    cdv_no = models.CharField('CDV No.', max_length=10, default='0')
    status = models.CharField('Audit 1', max_length=200, choices=CF_STATUS, default='Unliquidated')
    status2 = models.CharField('Audit 2', max_length=200, choices=CF_STATUS, default='For Review')
    create_date = models.DateTimeField('Date Created', auto_now_add=True)

    def __str__(self):
        return "%s" %(self.form_no)

    class Meta:
        verbose_name = 'Cash Fund'
        verbose_name_plural = 'Cash Fund'


class Liquidation(models.Model):
    base_budget = models.ForeignKey('accounting.CashBudget', verbose_name='Cash Request Slip No. (CRS No.)', related_name='liquidation', blank=True, null=True, on_delete = models.CASCADE)
    base_por = models.ForeignKey('accounting.OrderRequest', verbose_name='POR Trans #',related_name='por', blank=True, null=True, on_delete = models.SET_NULL)
    trans_date = models.DateField('Transaction Date (Actual):', default=timezone.now)
    project_site = models.ForeignKey(ProjectSite, related_name='liquidation_project_site', null=True, on_delete = models.SET_NULL)
    issued_by = models.ForeignKey(User, related_name='issued_by', on_delete = models.SET_NULL, null=True)

    item = models.ForeignKey('accounting.Item', related_name='item', null=True, blank=True, on_delete = models.SET_NULL)
    quantity = models.DecimalField('Quantity', max_digits=20, decimal_places=2, default=0)

    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)
    detail = models.CharField('Detail', max_length=200)
    supplier = models.ForeignKey('accounting.Supplier', related_name='supplier', blank=True, null=True, on_delete = models.SET_NULL)
    payment = models.CharField('Payment Mode', max_length=200, choices=PAYMENT_MODE, default='Cash')

    category = models.CharField('Account Category', max_length=200, choices=ACCOUNT_CATEGORY, default='Uncategorized')
    item_code = models.ForeignKey('accounting.ItemCode', related_name='item_liquidation', blank=True, on_delete = models.SET_NULL, null=True)
    trans_type = models.CharField('Type', max_length=200, choices=DEBIT_CREDIT, default='Debit')
    incoming_vat = models.DecimalField('Vat', max_digits=20, decimal_places=2, default=0, editable=False)
    vatable_sales = models.DecimalField('Vatable Sales', max_digits=20, decimal_places=2, editable=False)
    vat = models.BooleanField('Vatable?', default=False)

    create_date = models.DateTimeField('Date Created', auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.vat is True:
            self.incoming_vat = (self.amount/Decimal('1.12').quantize(Decimal('1.00')))*Decimal('.12').quantize(Decimal('1.00'))
            self.vatable_sales = self.amount - self.incoming_vat
        else:
            self.vatable_sales = self.amount
            self.incoming_vat = 0
        super(Liquidation, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" %(self.base_budget)

    class Meta:
        verbose_name = 'Liquidation'
        verbose_name_plural = 'Liquidations'





