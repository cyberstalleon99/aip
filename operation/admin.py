from django.contrib import admin
from django.shortcuts import redirect

from .models import (Project, Detail, WorkStat, Item, ProjectItem, Personnel,
                    Report, AllocatedExpense, MajorExpense, Gallery, Slides,
                    Billing, Reporting)

# Register your models here.

class PersonnelInline(admin.TabularInline):
    model = Personnel
    extra = 1

class WorkStatInline(admin.TabularInline):
    model = WorkStat
    exclude = ('create_date',)
    extra = 1

class ProjectItemInline(admin.TabularInline):
    model = ProjectItem
    exclude = ('create_date',)
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ProjectItemInline, self).get_formset(request, obj, **kwargs)

        formset.form.base_fields['item'].widget.can_change_related = False
        formset.form.base_fields['item'].widget.can_delete_related = False

        return formset

class AllocatedExpenseInline(admin.TabularInline):
    model = AllocatedExpense
    exclude = ('create_date',)
    extra = 0


class MajorExpenseInline(admin.TabularInline):
    model = MajorExpense
    exclude = ('create_date',)
    extra = 0

class SlidesInline(admin.TabularInline):
    model = Slides
    extra = 0

class DetailInline(admin.StackedInline):
    model = Detail
    exclude = ('create_date',)
    extra = 1

class BillingInline(admin.TabularInline):
    model = Billing
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code','project_name','project_detail','project_pic')
    list_filter = ('project_code','project_name')
    exclude = ('create_date',)
    inlines = [DetailInline,PersonnelInline,ProjectItemInline,WorkStatInline,
                AllocatedExpenseInline,MajorExpenseInline,
                BillingInline]

    def response_add(self, request, obj, post_url_continue=None):
        return redirect ('/operation/detail/%s' % (obj.id))

    def response_change(self, request, obj):
        return redirect ('/operation/detail/%s' % (obj.id))

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('base_project','project_id','award_date','expiry_date','contract_duration','contract_cost')
    list_filter = ('base_project','expiry_date')
    exclude = ('create_date',)

@admin.register(WorkStat)
class WorkStatAdmin(admin.ModelAdmin):
    list_display = ('base_project','date','planned', 'actual')
    list_filter = ('date',)
    exclude = ('create_date',)

@admin.register(MajorExpense)
class MajorExpenseAdmin(admin.ModelAdmin):
    list_display = ('base_project','date')
    list_filter = ('base_project','date')
    exclude = ('create_date',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_no','category','description')

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('base_project','office','title','name')
    list_filter = ('base_project','office','title')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('base_project','date','activity','issues','weather')
    list_filter = ('base_project','date','weather')
    exclude = ('create_date',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('base_project','date','title','detail')
    list_filter = ('base_project','date')
    inlines = [SlidesInline,]


@admin.register(Reporting)
class ReportingAdmin(admin.ModelAdmin):
    list_display = ('base_project','date','report_type', 'remarks','document')
    list_filter = ('date','report_type')
    exclude = ('create_date',)




