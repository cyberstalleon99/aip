from django.contrib import admin
from django.shortcuts import redirect

from .models import(ItemCode, Item, Supplier, OrderRequest, CashBudget,
            Liquidation, PriceList, Entry, FundRequest)


# Register your models here.

class LiquidationInline(admin.TabularInline):
    model = Liquidation
    extra = 0
    readonly_fields=('incoming_vat',)

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name__in=['Finance Level 2',]).exists():
            return ['create_date','base_budget']
        else:
            return ['create_date','category','item_code','trans_type',
                    'incoming_vat','vatable_sales','vat',]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(LiquidationInline, self).get_formset(request, obj, **kwargs)

        formset.form.base_fields['base_por'].widget.can_add_related = False
        formset.form.base_fields['base_por'].widget.can_change_related = False
        formset.form.base_fields['base_por'].widget.can_delete_related = False

        formset.form.base_fields['project_site'].widget.can_add_related = False
        formset.form.base_fields['project_site'].widget.can_change_related = False
        formset.form.base_fields['project_site'].widget.can_delete_related = False

        formset.form.base_fields['issued_by'].widget.can_add_related = False
        formset.form.base_fields['issued_by'].widget.can_change_related = False
        formset.form.base_fields['issued_by'].widget.can_delete_related = False

        formset.form.base_fields['item'].widget.can_add_related = False
        formset.form.base_fields['item'].widget.can_change_related = False
        formset.form.base_fields['item'].widget.can_delete_related = False

        formset.form.base_fields['supplier'].widget.can_add_related = False
        formset.form.base_fields['supplier'].widget.can_change_related = False
        formset.form.base_fields['supplier'].widget.can_delete_related = False

        #formset.form.base_fields['item_code'].widget.can_add_related = False
        #formset.form.base_fields['item_code'].widget.can_change_related = False
        #formset.form.base_fields['item_code'].widget.can_delete_related = False

        return formset

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['item_name',]
    list_display = ('item_name','general_name','item_category','item_unit','item_detail',)
    list_filter = ('item_name','general_name','item_category','item_unit')
    list_per_page = 10

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    search_fields = ['trans_date',]
    list_display = ('trans_date','entry_type','form_no','transaction_by','project_site', 'created_at', 'updated_at', 'created_by', 'modified_by')
    list_filter = ('entry_type','form_no','transaction_by','project_site')

@admin.register(FundRequest)
class FundRequestAdmin(admin.ModelAdmin):
    search_fields = ['trans_date','created_by']
    list_filter = ('created_by','request_to','project_site')
    list_display = ('trans_date','created_by','request_to','project_site','amount','remarks',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ('id','name','tin','address','contact')
    list_filter = ('name',)


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    search_fields = ['item','supplier','price']
    list_display = ('id','item','supplier','price')
    list_filter = ('item',)


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ('request_date','approved_at','purchased_at','request_form','request_by','project_site','item','quantity','details','status')
    list_filter = ('item','request_form','status','purchaser')
    inlines = [LiquidationInline]

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name__in=['Purchase Level 3',]).exists():
            return ['create_date']
        else:
            return ['create_date','status','purchaser']


@admin.register(CashBudget)
class CashBudgetAdmin(admin.ModelAdmin):
    search_fields = ['form_no',]
    list_display = ('trans_date','form_no','issued_by','issued_to','amount','detail','cdv_date','cdv_no','status')
    list_filter = ('trans_date','form_no','issued_by','issued_to')
    exclude = ('create_date',)
    inlines = [LiquidationInline,]

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name__in=['Accounting Level 2',]).exists():
            return ['create_date',]
        else:
            return ['cdv_date','cdv_no','status','status2',]


@admin.register(ItemCode)
class ItemCodeAdmin(admin.ModelAdmin):
    search_fields = ['item_code',]
    list_display = ('item_code','sc1','sc2','sc3',)
    list_filter = ('item_code',)

@admin.register(Liquidation)
class LiquidationAdmin(admin.ModelAdmin):
    search_fields = ['item_code', 'id']
    list_display = ('id','base_por','trans_date','project_site','issued_by','amount','item','detail','category','item_code','create_date')
    list_filter = ('id','base_por','item','category','item_code','issued_by')

    def get_exclude(self, request, obj=None):
        if request.user.groups.filter(name__in=['Accounting Level 1',]).exists():
            return ['create_date','quantity',]
        else:
            return ['create_date','category','item_code','trans_type',
                    'incoming_vat','vatable_sales','vat',]