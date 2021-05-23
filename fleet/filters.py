from .models import UtilizationReport, Travel, WorkOrder
import django_filters


class URFilter(django_filters.FilterSet):

    project_site = django_filters.CharFilter(lookup_expr='icontains')
    operator = django_filters.CharFilter(lookup_expr='icontains')
    unit_id = django_filters.CharFilter(lookup_expr='icontains')
    unit_type = django_filters.CharFilter(lookup_expr='icontains')
    activity = django_filters.CharFilter(lookup_expr='icontains')
    material = django_filters.CharFilter(lookup_expr='icontains')

    date = django_filters.DateFromToRangeFilter(field_name='date')
    class Meta:
        model = UtilizationReport
        fields = []

    def __init__(self, *args, **kwargs):
        super(URFilter, self).__init__(*args, **kwargs)

        initial_query = UtilizationReport.objects.order_by('-date')[:300]
        if self.data == {}:
            self.queryset = initial_query

class TravelFilter(django_filters.FilterSet):
    base_unit__body_no = django_filters.CharFilter(lookup_expr='icontains')
    date_start__date = django_filters.DateFromToRangeFilter(field_name='date_start')
    # driver__fullname = django_filters.CharFilter(lookup_expr='icontains')
    # requested_by__fullname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Travel
        fields = [
            'base_unit__body_no', 'requested_by', 'driver', 'date_start__date',
            'source', 'destination', 'status', 'trip'
        ]

    def __init__(self, *args, **kwargs):
        super(TravelFilter, self).__init__(*args, **kwargs)

        initial_query = Travel.objects.order_by('-create_date')[:100]
        if self.data == {}:
            self.queryset = initial_query


class WorkOrderFilter(django_filters.FilterSet):
    base_jo__jo_no = django_filters.CharFilter(lookup_expr='icontains')
    scope_work = django_filters.CharFilter(lookup_expr='icontains')
    work_done = django_filters.CharFilter(lookup_expr='icontains')
    remarks = django_filters.CharFilter(lookup_expr='icontains')
    date_start__date = django_filters.DateFromToRangeFilter(field_name='date_start')
    date_end__date = django_filters.DateFromToRangeFilter(field_name='date_end')

    class Meta:
        model = WorkOrder
        fields = [
            'base_jo__jo_no', 'scope_work', 'work_done', 'remarks', 'service_type', 'repair_cause',
            'wo_status', 'date_start__date', 'date_end__date'
        ]

    def __init__(self, *args, **kwargs):
        super(WorkOrderFilter, self).__init__(*args, **kwargs)

        initial_query = WorkOrder.objects.order_by('-create_date')[:100]
        if self.data == {}:
            self.queryset = initial_query



