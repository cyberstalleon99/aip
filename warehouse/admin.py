from django.contrib import admin
from .models import (Incoming, Outgoing)

from import_export.admin import ExportActionMixin

class OutgoingInline(admin.TabularInline):
    model = Outgoing
    ordering = ['-trans_date']
    extra = 0

@admin.register(Incoming)
class IncomingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id','trans_date','attachment','received_by','form_no','trans_no','project_site','item',
                    'quantity','details','unit_price', 'create_date', 'updated_at', 'created_by', 'modified_by')
    list_filter = ('id','trans_date','item','item__item_name','item__item_category','project_site','received_by')
    inlines = [OutgoingInline,]
    # raw_id_fields = ('item',)


    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name__in=['Warehouse Level 2',]).exists():
            return ['create_date', 'created_by', 'updated_at', 'modified_by']
        else:
            return ['create_date','unit_price','status', 'created_by', 'updated_at', 'modified_by']

@admin.register(Outgoing)
class OutgoingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('trans_date','base_in','trans_type','form_no','project_site','item',
                    'quantity','item_cost','details','released_by','released_to','unit','attachment', 'create_date', 'updated_at', 'created_by', 'modified_by')
    list_filter = ('base_in','trans_date','trans_type','form_no','project_site','unit','released_by')

    def item_cost(self, obj):
        try:
            return obj.base_in.unit_price
        except:
            return None

    def item(self, obj):
        try:
            return obj.base_in.item
        except:
            return None

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name__in=['Warehouse Level 2',]).exists():
            return ['create_date', 'created_by', 'updated_at', 'modified_by']
        else:
            return ['create_date', 'status', 'created_by', 'updated_at', 'modified_by']