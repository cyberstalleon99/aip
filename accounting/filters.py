from .models import PriceList, Liquidation, Entry, OrderRequest
import django_filters
from django.db.models import F

class PriceListFilter(django_filters.FilterSet):
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = PriceList
        fields = []

    def __init__(self, *args, **kwargs):
        super(PriceListFilter, self).__init__(*args, **kwargs)

        initial_query = PriceList.objects\
                .values('supplier__name','item__item_name')\
                .annotate(price=F('price'))\
                .annotate(date=F('create_date'))\
                .order_by('-create_date')[:5]
        if self.data == {}:
            self.queryset = initial_query


class PurchasedListFilter(django_filters.FilterSet):
    trans_date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Liquidation
        fields = ['id','base_por__request_form','project_site','issued_by','supplier','category']

    def __init__(self, *args, **kwargs):
        super(PurchasedListFilter, self).__init__(*args, **kwargs)

        initial_query = Liquidation.objects.order_by('-create_date')[:300]
        if self.data == {}:
            self.queryset = initial_query


class PurchasedMonitoringFilter(django_filters.FilterSet):
    create_date = django_filters.DateFromToRangeFilter(field_name='create_date')
    #request_date = django_filters.DateFromToRangeFilter(field_name='request_date')
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')
    project_site__project_code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OrderRequest
        fields = ['id','status','details']

    def __init__(self, *args, **kwargs):
        super(PurchasedMonitoringFilter, self).__init__(*args, **kwargs)

        initial_query = OrderRequest.objects.order_by('-request_date').annotate(actual_purchase=F('entry_por__created_at'))[:300]
        if self.data == {}:
            self.queryset = initial_query



class PurchasedEntryFilter(django_filters.FilterSet):
    trans_date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')
    project_site__project_code = django_filters.CharFilter(lookup_expr='icontains')
    subcon__group_name = django_filters.CharFilter(lookup_expr='icontains')

    transaction_by__first_name = django_filters.CharFilter(lookup_expr='icontains')
    created_by__first_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Entry
        fields = ['id','form_no','status','remarks']

    def __init__(self, *args, **kwargs):
        super(PurchasedEntryFilter, self).__init__(*args, **kwargs)

        initial_query = Entry.objects\
                .exclude(item__isnull=True).order_by('-created_at')[:300]
        if self.data == {}:
            self.queryset = initial_query


class CreditEntryFilter(django_filters.FilterSet):
    trans_date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')
    project_site__project_code = django_filters.CharFilter(lookup_expr='icontains')
    subcon__group_name = django_filters.CharFilter(lookup_expr='icontains')

    transaction_by__first_name = django_filters.CharFilter(lookup_expr='icontains')
    created_by__first_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Entry
        fields = ['id','form_no','status','remarks']

    def __init__(self, *args, **kwargs):
        super(CreditEntryFilter, self).__init__(*args, **kwargs)

        initial_query = Entry.objects.filter(utang=True)\
                .exclude(item__isnull=True).order_by('-created_at')[:300]
        if self.data == {}:
            self.queryset = initial_query


class CancelledPurchaseFilter(django_filters.FilterSet):
    request_date = django_filters.DateFromToRangeFilter(field_name='request_date')
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')
    project_site__project_code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OrderRequest
        fields = ['id','details']

    def __init__(self, *args, **kwargs):
        super(CancelledPurchaseFilter, self).__init__(*args, **kwargs)

        initial_query = OrderRequest.objects.filter(status = 'Canceled').order_by('-request_date')[:300]
        if self.data == {}:
            self.queryset = initial_query


class JournalEntryFilter(django_filters.FilterSet):
    trans_date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    project_site__project_code = django_filters.CharFilter(lookup_expr='icontains')
    account_code__sc1 = django_filters.CharFilter(lookup_expr='icontains')
    subcon__group_name = django_filters.CharFilter(lookup_expr='icontains')
    transaction_by__first_name = django_filters.CharFilter(lookup_expr='icontains')
    created_by__first_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Entry
        fields = ['id','form_no','project_site','status','remarks']

    def __init__(self, *args, **kwargs):
        super(JournalEntryFilter, self).__init__(*args, **kwargs)

        initial_query = Entry.objects.order_by('-created_at')[:100]
        if self.data == {}:
            self.queryset = initial_query



