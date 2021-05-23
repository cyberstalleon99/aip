from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import (BasicProfile, ProjectSite, Outsider, EmployeeProfile, Accounts, Family,
                    WorkHistory, Leave, Loans, Payment, FileDocument, Education, Attachment,
                    Subcon, Department)

class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    fk_name = "base_profile"
    extra = 1

class AccountInline(admin.TabularInline):
    model = Accounts
    extra = 0

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class FamilyInline(admin.TabularInline):
    model = Family
    extra = 0

class WorkHistoryInline(admin.TabularInline):
    model = WorkHistory
    extra = 0

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

class LeaveInline(admin.TabularInline):
    model = Leave
    fk_name = 'base_profile'
    exclude = ('create_date',)
    extra = 0

class LoanInline(admin.TabularInline):
    model = Loans
    exclude = ('create_date',)
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    exclude = ('create_date',)
    extra = 0

# Register your models here.
@admin.register(BasicProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('fname','lname','age','civil_status','dbirth','mobile','email')
    list_filter = ('fname','lname','gender','civil_status','employee_profile__project_site',
                    'employee_profile__designation')
    exclude = ('create_date',)
    inlines = [EmployeeProfileInline, AccountInline, EducationInline,
                FamilyInline, WorkHistoryInline, LeaveInline, LoanInline, AttachmentInline]

@admin.register(ProjectSite)
class ProjectSiteAdmin(admin.ModelAdmin):
    list_display = ('id','project_code','name','branch','project_status','project_type')
    list_filter = ('project_code','name','branch','project_status','project_type')

@admin.register(Outsider)
class OutsiderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','details')

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id_no','base_profile','employment_status','employment_type','date_hired','designation','branch')
    list_filter = ('employment_status','employment_type','designation','branch','project_site')

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ('base_profile','title','account')
    list_filter = ('base_profile','title')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school','level','start_year','end_year','remarks')
    list_filter = ('school','level')

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('relation','name','contact_no')

@admin.register(WorkHistory)
class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ('base_profile','company_name','designation','start_year','end_year')
    list_filter = ('base_profile','company_name','designation')

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    search_fields = ('base_profile__fname', 'base_profile__lname')
    list_display = ('base_profile','date_from','date_to','leave_type','reason','approval_super','approved_by_super','approval','approved_by', 'create_date')
    list_filter = ('base_profile', 'leave_type', 'approval_super', 'approval', 'create_date')
    exclude = ('create_date',)

@admin.register(Loans)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('base_profile','trans_date','amount','detail','status','approved_by')
    list_filter = ('base_profile','status','approved_by')
    exclude = ('create_date',)
    inlines = [PaymentInline,]

@admin.register(FileDocument)
class FileDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_title','document_type','issued_date','expiry_date','doc_image')
    list_filter = ('document_title','document_type','status')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('base_profile','document_title','document_type','issued_date','expiry_date','doc_file')
    list_filter = ('base_profile','document_title','document_type')

@admin.register(Subcon)
class SubconAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name','boss','remarks', 'create_date')
    list_filter = ('group_name','boss')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head')
    list_filter = ('head',)






