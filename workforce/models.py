from django.db import models
from django.utils import timezone
from datetime import date, datetime
from django.core.mail import send_mail

from django.contrib.auth.models import User

from workforce.constants import (GENDER, CIVIL_STATUS, TITLE, RELIGION, EMPLOYMENT_STATUS,
            EMPLOYMENT_TYPE, DESIGNATION, BRANCH, RELATION, APPROVAL, APPROVAL_SUPERVISOR, LOAN_APPROVAL,
            LEAVE, DOC_TYPE, ATTACH_TYPE, PROJECT_STATUS, PROJECT_TYPE, FILE_STAT, EVAL_STAT)

SUBCON_STATUS = (
    ('Active','Active'),
    ('Completed','Completed'),
)

# Create your models here.
class BasicProfile(models.Model):
    account = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    fname = models.CharField('First Name', max_length=200)
    mname = models.CharField('Middle Name', max_length=200)
    lname = models.CharField('Last Name', max_length=200)
    gender = models.CharField('Gender', max_length=200, choices=GENDER)
    civil_status = models.CharField('Civil Status', max_length=200, choices=CIVIL_STATUS)
    religion = models.CharField('Religion', max_length=200, choices=RELIGION)
    dbirth = models.DateField('Date of Birth', default=timezone.now)
    birthplace = models.CharField('Birth Place', max_length=200, blank=True, default='')
    mobile = models.DecimalField('Primary', max_digits=20, decimal_places=0, default=0)
    mobile2 = models.DecimalField('Secondary', max_digits=20, decimal_places=0, default=0)
    email = models.EmailField('Email', blank=True)
    home_address = models.CharField('Home Address', max_length=1000, blank=True, default='')
    current_address = models.CharField('Current Address', max_length=1000, blank=True, default='')
    profile_pic = models.ImageField('Profile Pic', upload_to='profile_pic', default='profile_pic/default.png')
    title = models.CharField('Title', max_length=200, choices=TITLE)

    height = models.DecimalField('Height(m)', max_digits=20, decimal_places=2, default=0)
    weight = models.DecimalField('Weight(kg)', max_digits=20, decimal_places=2, default=0)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def fullname(self):
        return "%s %s %s %s" %(self.title, self.fname, self.mname, self.lname)

    def age(self):
        today = date.today()
        return today.year - self.dbirth.year - ((today.month, today.day) < (self.dbirth.month, self.dbirth.day))

    def bmi(self):
        try:
            return round(self.weight/((self.height)**2),2)
        except:
            return None

    def __str__(self):
        return "%s %s" %(self.fname, self.lname)

    class Meta:
        verbose_name = 'Basic Profile'
        verbose_name_plural = 'Employees'


class ProjectSite(models.Model):
    project_code = models.CharField('Project Code', db_index=True, max_length=40)
    name = models.CharField('Project Name', max_length=200)
    branch = models.CharField('Project Area', max_length=200, blank=True, choices=BRANCH)
    project_status = models.CharField('Status', max_length=200, default='Completed', choices=PROJECT_STATUS)
    project_type = models.CharField('Type', max_length=200, default='Project', choices=PROJECT_TYPE)


    lat = models.DecimalField('Lat', max_digits=9, decimal_places=6, default=0)
    lon = models.DecimalField('Lon', max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return "%s" %(self.project_code)

    class Meta:
        verbose_name = 'Project Site'
        verbose_name_plural = 'Project Site'


class Outsider(models.Model):
    name = models.CharField('Name', max_length=200)
    details = models.TextField('Details',)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = 'Outsider'
        verbose_name_plural = 'Outsiders'

# **************************************************************
# START dongilay
# **************************************************************
class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey(BasicProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
# **************************************************************
# END dongilay
# **************************************************************

class EmployeeProfile(models.Model):
    base_profile = models.OneToOneField('workforce.BasicProfile', related_name='employee_profile', on_delete = models.CASCADE)
    department = models.ForeignKey(Department, related_name='department', on_delete=models.SET_NULL, null=True, blank=True)
    supervisor = models.ForeignKey(BasicProfile, related_name='supervisor', on_delete=models.SET_NULL, null=True, blank=True)
    # department = models.OneToOneField(Department, related_name='department', on_delete=models.SET_NULL, null=True, blank=True)
    # supervisor = models.OneToOneField(BasicProfile, related_name='supervisor', on_delete=models.SET_NULL, null=True, blank=True)
    id_no = models.CharField('ID No.', max_length=40)
    employment_status = models.CharField('Employment Status', max_length=40, choices=EMPLOYMENT_STATUS)
    employment_type = models.CharField('Employement Type', max_length=40, choices=EMPLOYMENT_TYPE)
    date_hired = models.DateField('Date Hired', default=timezone.now)
    designation = models.CharField('Designation', max_length=200, choices=DESIGNATION)
    branch = models.CharField('Branch', max_length=200, blank=True, choices=BRANCH)
    project_site = models.ForeignKey('workforce.ProjectSite', related_name='site', on_delete = models.CASCADE)
    end_probation = models.DateField('End of Probation', blank=True, null=True)
    regularization = models.DateField('Date of Regularization', blank=True, null=True)
    separation = models.DateField('Date of Separation', blank=True, null=True)
    evaluation = models.CharField('Evaluation', max_length=40, default='Done', choices=EVAL_STAT)
    referral = models.CharField('Referral', max_length=200, blank=True, default='')

    def __str__(self):
        return "%s" %(self.id_no)

    class Meta:
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profile'


class Accounts(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='accounts', on_delete = models.CASCADE)
    title = models.CharField('Title', max_length=40, blank=True)
    account = models.CharField('Account No.', max_length=40, blank=True)

    def __str__(self):
        return "%s" %(self.title)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Education(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='education', on_delete = models.CASCADE)

    level = models.CharField('Level of Attainment', max_length=500)
    school = models.CharField('School', max_length=500)
    start_year = models.DateField('Start Year')
    end_year = models.DateField('End Year')
    remarks = models.CharField('Remarks', max_length=500)

    def __str__(self):
        return "%s" %(self.school)

    class Meta:
        verbose_name = 'Educational Background'
        verbose_name_plural = 'Educational Background'


class Family(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='family', on_delete = models.CASCADE)
    name = models.CharField('Name', max_length=500)
    relation = models.CharField('Relation', max_length=200, choices=RELATION)
    contact_no = models.DecimalField('Mobile No.', blank=True, null=True, max_digits=20, decimal_places=0)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = 'Family & Dependents'
        verbose_name_plural = 'Family & Dependents'


class WorkHistory(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='work_history', on_delete = models.CASCADE)
    company_name = models.CharField('Company Name', max_length=200)
    designation = models.CharField('Designation', max_length=200)
    start_year = models.DateField('Start Year', default=timezone.now)
    end_year = models.DateField('End Year', default=timezone.now)
    work_description = models.CharField('Work Description', max_length=1000)
    supervisor = models.CharField('Immediate Supervisor', max_length=200)
    contact_no = models.DecimalField('Mobile No.', max_digits=20, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return "%s" %(self.company_name)

    class Meta:
        verbose_name = 'Work History'
        verbose_name_plural = 'Work History'


class Leave(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='leave_record', on_delete = models.CASCADE)
    date_from = models.DateField('Start Date')
    date_to = models.DateField('End Date')
    leave_type = models.CharField('Leave', max_length=200, choices=LEAVE)
    reason = models.CharField('Remarks', max_length=500)
    tots_days = models.DecimalField('Total Days', max_digits=20, decimal_places=1, null=True, blank=True, default=0)
    attachment = models.FileField('Upload Leave', upload_to='leave_files', blank=True, default=' ')

    approval_super = models.CharField('Status (Supervisor)', max_length=200, choices=APPROVAL_SUPERVISOR, default='For Approval', null=True, blank=True)
    approved_by_super = models.ForeignKey('workforce.BasicProfile', verbose_name="Approved by (Supervisor)", related_name='approved_by_super', on_delete=models.CASCADE, blank=True, null=True)
    date_approved_super = models.DateField(verbose_name="Date Approved (Supervisor)", blank=True, null=True)
    remarks_super = models.TextField('Remarks (Supervisor)', null=True, blank=True)

    approval = models.CharField('Status (Admin)', max_length=200, choices=APPROVAL, default='For Approval', null=True, blank=True)
    approved_by = models.ForeignKey('workforce.BasicProfile', verbose_name="Approved by (Admin)", related_name='approved_by', on_delete=models.CASCADE, null=True, blank=True)
    date_approved = models.DateField(verbose_name="Date Approved (Admin)", null=True, blank=True)
    remarks = models.TextField('Remarks (Admin)', null=True, blank=True)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    @property
    def total_days(self):
        return (self.date_to - self.date_from).days + 1

    def __str__(self):
        return "%s" %(self.base_profile)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         supervisor = str(self.approved_by.email)
    #         subject = 'Leave Application: ' + str(self.base_profile)
    #         message = 'An application for leave is on que, and needs your attention! Link: https://eakdev.pythonanywhere.com/workforce/leaves/'
    #         send_mail(
    #             subject,
    #             message,
    #             'aip911dispatch@gmail.com',
    #             ['erickiser87@gmail.com','eillensybellepeil.aip@gmail.com','qhennyfuyag.aip@gmail.com','penelopelawangen.aip@gmail.com',supervisor],
    #             fail_silently=False,
    #         )
    #     super(Leave, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Leave Monitoring'
        verbose_name_plural = 'Leave Monitoring'

class Loans(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='loan_record', on_delete = models.CASCADE)
    trans_date = models.DateField('Transaction Date:', default=timezone.now)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)
    detail = models.CharField('Detail', max_length=200)
    status = models.CharField('Status', max_length=200, choices=LOAN_APPROVAL, default='For Approval')
    approved_by = models.ForeignKey(User, related_name='approved_by_loan', on_delete = models.SET_NULL, null=True)
    doc_file = models.FileField('Form', upload_to='loan_files', blank=True, default=' ')

    create_date = models.DateTimeField('Date Created', auto_now_add=True)

    def __str__(self):
        return "%s" %(self.trans_date)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


class Payment(models.Model):
    base_loan = models.ForeignKey('workforce.Loans', related_name='loan_payment', on_delete = models.CASCADE)
    trans_date = models.DateField('Transaction Date:', default=timezone.now)
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2, default=0)
    detail = models.CharField('Detail', max_length=200)

    create_date = models.DateTimeField('Date Created', auto_now_add=True)

    def __str__(self):
        return "%s" %(self.trans_date)

    class Meta:
        verbose_name = 'Loan Payment'
        verbose_name_plural = 'Loan Payments'


class FileDocument(models.Model):
    document_title = models.CharField('Title', max_length=200)
    document_type = models.CharField('Document Type', max_length=200, choices=DOC_TYPE)
    issued_date = models.DateField('Date Issued', default=timezone.now)
    expiry_date = models.DateField('Expiry Date', default=timezone.now)
    doc_image = models.ImageField('Scanned Document', upload_to='doc_files', blank=True, default='profile_pic/default.png')
    status = models.CharField('Status', max_length=50, default='Renewed', choices=FILE_STAT)
    remarks = models.CharField('Remarks', max_length=200, default='')

    def days2expiry(self):
        return (self.expiry_date - date.today()).days +1

    def __str__(self):
        return "%s" %(self.document_title)

    class Meta:
        verbose_name = 'Documents'
        verbose_name_plural = 'Documents'



class Attachment(models.Model):
    base_profile = models.ForeignKey('workforce.BasicProfile', related_name='attachment_record', on_delete = models.CASCADE)
    document_title = models.CharField('Title', max_length=200)
    document_type = models.CharField('Document Type', max_length=200, choices=ATTACH_TYPE)
    issued_date = models.DateField('Date Issued', default=timezone.now)
    expiry_date = models.DateField('Expiry Date', default=timezone.now)
    doc_file = models.FileField('Document', upload_to='memo_files', blank=True, default='profile_pic/default.png')

    def days2expiry(self):
        return (self.expiry_date - date.today()).days +1

    def __str__(self):
        return "%s" %(self.document_title)

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

class Subcon(models.Model):
    group_name = models.CharField('Group Name', max_length=200)
    boss = models.CharField('Leader', max_length=200)
    project_site = models.ForeignKey('workforce.ProjectSite', related_name='subcon_site', blank=True, null=True, on_delete = models.CASCADE)
    remarks = models.TextField('Remarks', max_length=200, default='')
    status = models.CharField('Status', max_length=200, default='Completed', choices=SUBCON_STATUS)

    create_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return "%s %s" %(self.group_name, self.group_name)

    class Meta:
        verbose_name = 'Subcon Group'
        verbose_name_plural = 'Subcon Groups'



















