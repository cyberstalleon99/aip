from .models import (Incoming, Outgoing)
from django.db.models import Avg,Sum,F,Q,When,Case,Count,IntegerField, FloatField, OuterRef

import django_filters


class IncomingFilter(django_filters.FilterSet):
    trans_date__date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    item__general_name = django_filters.CharFilter(lookup_expr='icontains')
    item__item_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Incoming
        fields = [
            'project_site', 'item__item_name', 'trans_date__date',
            'received_by', 'item__item_category',
            'item__general_name',
            ]

    def __init__(self, *args, **kwargs):
        super(IncomingFilter, self).__init__(*args, **kwargs)

        initial_query = Incoming.objects\
            .select_related('received_by','project_site','item')\
            .annotate(tot_out=Sum('out__quantity'))\
            .annotate(current_count=F('quantity')-F('tot_out'))\
            .filter(current_count__gt=0)\
            .order_by('-trans_date')[:100]


        # initial_query = initial_query.exclude(current_count__lte=0)[:100]

        if self.data == {}:
            self.queryset = initial_query


class OutgoingFilter(django_filters.FilterSet):
    trans_date = django_filters.DateFromToRangeFilter(field_name='trans_date')
    base_in__item__item_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Outgoing
        fields = [
            'base_in__project_site', 'base_in__item__item_name', 'trans_date',
            'released_by', 'trans_type', 'base_in__item__item_category',
            'base_in__item__general_name','released_to','unit',
            ]

    def __init__(self, *args, **kwargs):
        super(OutgoingFilter, self).__init__(*args, **kwargs)

        initial_query = Outgoing.objects.order_by('-trans_date')[:100]
        if self.data == {}:
            self.queryset = initial_query