from .models import Transaction
import django_filters


class FuelFilter(django_filters.FilterSet):

    fwf = django_filters.CharFilter(lookup_expr='icontains')
    remarks = django_filters.CharFilter(lookup_expr='icontains')

    trans_date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    class Meta:
        model = Transaction
        fields = ['trans_type','fwf','processed_by','tank_site','project_site','unit','trans_date','remarks']

    def __init__(self, *args, **kwargs):
        super(FuelFilter, self).__init__(*args, **kwargs)

        initial_query = Transaction.objects.order_by('-trans_date')[:300]
        if self.data == {}:
            self.queryset = initial_query
