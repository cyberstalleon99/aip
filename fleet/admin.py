from django.contrib import admin
from django.shortcuts import redirect
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import (UnitProfile, Travel, Operator, JobOrder, WorkOrder,
                    Manpower, Attachment, Slides, JOImage, Tools, Delivery,
                    UtilizationReport)

from import_export.admin import ExportActionMixin


class OperatorInline(admin.TabularInline):
    model = Operator
    extra = 0

class TravelInline(admin.TabularInline):
    model = Travel
    extra = 0

class ToolsInline(admin.TabularInline):
    model = Tools
    extra = 0

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

class WorkOrderInline(admin.StackedInline):
    model = WorkOrder
    exclude = ('create_date',)
    extra = 0

class ManpowerInline(admin.TabularInline):
    model = Manpower
    extra = 1

class SlidesInline(admin.TabularInline):
    model = Slides
    extra = 1

class JOImageInline(admin.TabularInline):
    model = JOImage
    extra = 1



@admin.register(UnitProfile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['body_no',]
    list_display = ('id','body_no','plate_no','unit_desc','operator','project_site','status')
    list_filter = ('project_site','status')
    exclude = ('create_date',)
    inlines = [OperatorInline, TravelInline, ToolsInline, AttachmentInline, SlidesInline]

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('operator','base_unit','date_start','date_end')
    list_filter = ('operator','base_unit','date_start','date_end')

@admin.register(UtilizationReport)
class UtilizationReportAdmin(admin.ModelAdmin):
    list_display = ('date','unit_id','operator','project_site','start_hour','end_hour','twh','activity','material','load','remarks')
    list_filter = (
        ('date', DateRangeFilter),'unit_id','operator','project_site','activity','material'
        )

@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ('id', 'requested_by', 'base_unit','driver','date_start', 'source', 'destination', 'note', 'status', 'started_at', 'arrived_at', 'returning_at', 'returned_at')
    list_per_page = 20
    list_filter = ('driver','date_start','note','base_unit','status')
    search_fields = ('driver__fname', 'driver__lname', 'base_unit__body_no', 'base_unit__plate_no', 'requested_by__fname', 'requested_by__lname')
    # exclude = ('create_date', 'started_at', 'arrived_at', 'returning_at', 'returned_at',)

    def response_add(self, request, post_url_continue=None):
        return redirect ('/fleet/travel/')

    def response_change(self, request, obj, post_url_continue=None):
        if '_continue' in request.POST:
            return super(TravelAdmin, self).response_change(request, obj)
        else:
            return redirect ('/fleet/travel/')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('create_date','request_by','source','destination','description','status','remarks')
    list_filter = ('request_by','source','destination','status')
    exclude = ('create_date',)

    def response_add(self, request, post_url_continue=None):
        return redirect ('/fleet/padala/')

    def response_change(self, request, obj, post_url_continue=None):
        if '_continue' in request.POST:
            return super(DeliveryAdmin, self).response_change(request, obj)
        else:
            return redirect ('/fleet/padala/')

@admin.register(JobOrder)
class JobOrderAdmin(admin.ModelAdmin):
    list_display = ('base_unit','jo_no','create_date','request_date','site','request_by','detail','smr','kmr','status')
    list_filter = ('request_date','site','request_by','base_unit','status')
    exclude = ('create_date',)
    inlines = [JOImageInline,WorkOrderInline]
    save_as = True

@admin.register(WorkOrder)
class WorkOrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('base_jo','date_start','date_end','service_type','repair_cause','scope_work','wo_status','site','unit','operator','running_days')
    list_filter = ('base_jo','date_start','date_end','service_type','repair_cause','wo_status','base_jo__base_unit','base_jo__base_unit__operator')
    exclude = ('create_date',)
    inlines = [ManpowerInline,]
    save_as = True

    def site(self, obj):
        try:
            return obj.base_jo.site
        except:
            return None

    def unit(self, obj):
        try:
            return obj.base_jo.base_unit
        except:
            return None

    def operator(self, obj):
        try:
            return obj.base_jo.base_unit.operator
        except:
            return None
