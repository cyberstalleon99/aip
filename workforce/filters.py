from django.contrib.admin.models import LogEntry
from django.db.models import Avg,Sum,F,Q,When,Case,Count,IntegerField, FloatField, OuterRef

import django_filters
import datetime


class LogFilter(django_filters.FilterSet):
    action_time__date = django_filters.DateFromToRangeFilter(field_name='action_time')
    user__first_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = LogEntry
        fields = ['content_type',]

    def __init__(self, *args, **kwargs):
        super(LogFilter, self).__init__(*args, **kwargs)

        today = datetime.date.today()

        initial_query = LogEntry.objects.filter(action_time__date=today)

        if self.data == {}:
            self.queryset = initial_query
