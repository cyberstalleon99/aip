from django.db.models import Avg,Sum,F,Q,When,Case,Count,IntegerField, FloatField, OuterRef
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import date
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView, ListView, CreateView, UpdateView

from warehouse.models import (Incoming, Outgoing)
from workforce.models import (ProjectSite,)
from fuel.models import (Transaction,)
from accounting.models import (OrderRequest, Liquidation)

from itertools import zip_longest
from django.shortcuts import render
from .filters import IncomingFilter, OutgoingFilter
from .forms import IncomingForm, OutgoingForm

# **************************************************************
# START dongilay
# **************************************************************

from .helpers import add_log, change_log

# **************************************************************
# END dongilay
# **************************************************************

current_date = timezone.now()

class DashView(ListView):
    model = ProjectSite
    template_name = 'warehouse/dash_page.html'

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)

        project_sites = ProjectSite.objects.all()

        context['main_warehouse'] = ProjectSite.objects.filter(project_type='Warehouse')
        context['project_warehouse'] = ProjectSite.objects.filter(project_type='Project').filter(project_status='Under Construction')

        context['daily_in'] = project_sites.filter(in_project_site__trans_date=date.today()).values('in_project_site__project_site').annotate(count_in = Count('in_project_site'))
        context['daily_out'] = project_sites.values('in_project_site__project_site').annotate(count_out = Count(Case(When(in_project_site__out__trans_date = date.today(), then=1), output_field=IntegerField())))

        context['pending'] = project_sites.filter(or_project_site__status='For Approval').values('or_project_site__project_site').annotate(pending = Count('or_project_site'))
        context['active'] = project_sites.filter(or_project_site__status='On-Process').values('or_project_site__project_site').annotate(on_process = Count('or_project_site'))
        context['purchased'] = project_sites.filter(liquidation_project_site__trans_date=date.today()).values('liquidation_project_site__project_site').annotate(purchase_today = Count('liquidation_project_site'))

        return context

# **************************************************************
# START dongilay
# **************************************************************

def get_incoming_left(incoming):
    outgoings = Outgoing.objects.filter(base_in=incoming)
    outgoings_quant = outgoings.aggregate(Sum('quantity'))['quantity__sum']

    incoming_left = 0

    if outgoings_quant:
        incoming_left = incoming.quantity - outgoings_quant
    else:
        incoming_left = incoming.quantity

    return incoming_left

# Incoming CRUD
class NewIncomingView(LoginRequiredMixin, CreateView):
    model = Incoming
    template_name = 'warehouse/new_incoming_form.html'
    form_class = IncomingForm

    def get_context_data(self, **kwargs):
        context = super(NewIncomingView,self).get_context_data(**kwargs)

        if 'pk' in self.kwargs:
            context['project_site'] = ProjectSite.objects.get(id=self.kwargs['pk'])
        else:
            context['project_site'] = None

        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('warehouse:detail_incoming', args=(self.object.id,))
        return url

class UpdateIncomingView(LoginRequiredMixin, UpdateView):
    model = Incoming
    template_name = 'warehouse/new_incoming_form.html'
    form_class = IncomingForm

    def form_valid(self, form):
        self.form = form
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('warehouse:detail_incoming', args=(self.object.id,))

class DetailIncomingView(LoginRequiredMixin, DetailView):
    model = Incoming
    template_name = 'warehouse/incoming_detail.html'
    context_object_name = 'incoming_detail'

    def get_object(self):
        incoming_id =self.kwargs.get("pk")
        return get_object_or_404(Incoming, id=incoming_id)

    def get_context_data(self, **kwargs):
        context = super(DetailIncomingView,self).get_context_data(**kwargs)

        outgoings = Outgoing.objects.filter(base_in=self.get_object())
        context['outgoings'] = outgoings
        context['total_outgoings'] = outgoings.aggregate(Sum('quantity'))['quantity__sum']
        context['incoming'] = self.get_object()
        context['available_incoming'] = get_incoming_left(self.get_object())

        return context

# Outgoing CRUD
class NewOutgoingView(LoginRequiredMixin, CreateView):
    model = Outgoing
    template_name = 'warehouse/outgoing_form.html'
    form_class = OutgoingForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NewOutgoingView,self).get_context_data(**kwargs)
        incoming = Incoming.objects.get(id=self.kwargs['pk'])

        context['incoming'] = incoming
        context['available_incoming'] = get_incoming_left(incoming)

        return context

    def get_success_url(self, **kwargs):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('warehouse:detail_incoming', kwargs={'pk': self.kwargs['pk']})
        return url

class UpdateOutgoingView(LoginRequiredMixin, UpdateView):
    model = Outgoing
    template_name = 'warehouse/outgoing_form.html'
    form_class = OutgoingForm

    def form_valid(self, form):
        self.form = form
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateOutgoingView,self).get_context_data(**kwargs)
        incoming = Incoming.objects.get(id=self.kwargs['incoming_id'])

        context['incoming'] = incoming
        context['available_incoming'] = get_incoming_left(incoming)

        return context

    def get_success_url(self, **kwargs):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        url = reverse_lazy('warehouse:detail_incoming', kwargs={'pk': self.kwargs['incoming_id']})
        return url

# **************************************************************
# END dongilay
# **************************************************************

class StatsView(ListView):
    model = Incoming
    template_name = 'warehouse/stats_page.html'
    context_object_name = 'stats_list'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)

        context['stats'] = Incoming.objects\
                .values('project_site__project_code')\
                .annotate(in_quantity=Sum(F('quantity')*F('unit_price')))\
                .annotate(out_quantity=Sum(F('out__quantity')*F('unit_price')))\
                .annotate(site_value=F('in_quantity')-F('out_quantity'))

        context['stats_per_class'] = Incoming.objects\
                .values('item__item_category')\
                .annotate(out_value=Sum(F('out__quantity')*F('unit_price'), filter=(Q(out__trans_type='Outgoing'))))

        context['stats_per_name'] = Incoming.objects\
                .values('item__general_name')\
                .annotate(out_value=Sum(F('out__quantity')*F('unit_price'), filter=(Q(out__trans_type='Outgoing'))))
        context['stat_per_item'] = Outgoing.objects\
                .values('unit__body_no')\
                .annotate(out_value=Sum(F('quantity')*F('base_in__unit_price'), filter=(Q(trans_type='Outgoing'))))

        return context


#Warehouse Detail For Main Warehouse
class DetailViewMain(DetailView):
    model = ProjectSite
    template_name = 'warehouse/detail_page_main.html'
    context_object_name = 'site_purchase'

    def get_context_data(self, **kwargs):
        context = super(DetailViewMain, self).get_context_data(**kwargs)

        incoming = Incoming.objects.filter(project_site__id=self.object.id).select_related('received_by','project_site','item')
        outgoing = Outgoing.objects\
                .filter(base_in__project_site__id=self.object.id)\
                .select_related('project_site','released_by','released_to','released_out','unit')

        current_in = incoming.values('item__item_name').annotate(tot_in=Sum('quantity')).annotate(cat_in=F('item__item_category'))
        current_out = incoming.values('item__item_name').annotate(tot_out=Sum('out__quantity')).annotate(cat_out=F('item__item_category'))
        context['current'] = [{**u, **v} for u, v in zip_longest(current_in, current_out, fillvalue={})]

        #cement
        cement_in = incoming.filter(item__general_name__contains="Cement @").values('item__general_name').annotate(tot_in=Sum('quantity'))
        cement_out = incoming.filter(item__general_name__contains="Cement @").values('item__general_name').annotate(tot_out=Sum('out__quantity'))
        context['cement'] = [{**u, **v} for u, v in zip_longest(cement_in, cement_out, fillvalue={})]

        #RSB
        rsb_in = incoming.filter(item__item_name__contains="RSB").values('item__item_name').annotate(tot_in=Sum('quantity'))
        rsb_out = incoming.filter(item__item_name__contains="RSB").values('item__item_name').annotate(tot_out=Sum('out__quantity'))
        context['rsb'] = [{**u, **v} for u, v in zip_longest(rsb_in, rsb_out, fillvalue={})]

        #Lumber
        lumber_in = incoming.filter(item__item_name__contains="Lumber").values('item__item_name').annotate(tot_in=Sum('quantity'))
        lumber_out = incoming.filter(item__item_name__contains="Lumber").values('item__item_name').annotate(tot_out=Sum('out__quantity'))
        context['lumber'] = [{**u, **v} for u, v in zip_longest(lumber_in, lumber_out, fillvalue={})]

        #Aggregates
        agg_in = incoming.filter(item__item_category="Aggregates").values('item__item_name').annotate(tot_in=Sum('quantity'))
        agg_out = incoming.filter(item__item_category="Aggregates").values('item__item_name').annotate(tot_out=Sum('out__quantity'))
        context['aggregates'] = [{**u, **v} for u, v in zip_longest(agg_in, agg_out, fillvalue={})]


        context['main_in'] = incoming.annotate(tot_out=Sum('out__quantity'))\
                .annotate(current_count=F('quantity')-F('tot_out'))\
                .order_by('-trans_date')[:300]
        context['main_out'] = outgoing.order_by('-trans_date')[:300]

        #issue tracker
        context['no_price'] = incoming.filter(unit_price=0).count()
        context['no_attach_in'] = incoming.filter(Q(attachment="") | Q(attachment=None)).count()
        context['no_attach_out'] = outgoing.filter(Q(attachment="") | Q(attachment=None)).count()
        context['x_form_in'] = incoming.exclude(form_no__regex=r'^[A-Z]*-[0-9]{2}-[0-9]*').count()
        context['x_form_out'] = outgoing.exclude(form_no__regex=r'^[A-Z]*-[0-9]{2}-[0-9]*').count()
        context['negatives'] = incoming.annotate(tot_out=Sum('out__quantity'))\
                .annotate(current_count=F('quantity')-F('tot_out'))\
                .filter(current_count__lt=0)\
                .count()


        return context


#Warehouse Detail For Project Sites
class DetailView(DetailView):
    model = ProjectSite
    template_name = 'warehouse/detail_page.html'
    context_object_name = 'site_purchase'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        incoming = Incoming.objects.filter(project_site__id=self.object.id).select_related('received_by','project_site','item')
        outgoing = Outgoing.objects\
                .filter(base_in__project_site__id=self.object.id)\
                .select_related('project_site','released_by','released_to','released_out','unit')

        current_in = incoming.values('item__item_name').annotate(tot_in=Sum('quantity')).annotate(cat_in=F('item__item_category'))
        current_out = incoming.values('item__item_name').annotate(tot_out=Sum('out__quantity')).annotate(cat_out=F('item__item_category'))
        context['current'] = [{**u, **v} for u, v in zip_longest(current_in, current_out, fillvalue={})]

        #cement
        cement_in = incoming.filter(item__general_name__contains="Cement @").values('item__general_name').annotate(tot_in=Sum('quantity'))
        cement_out = incoming.filter(item__general_name__contains="Cement @").values('item__general_name').annotate(tot_out=Sum('out__quantity'))
        context['cement'] = [{**u, **v} for u, v in zip_longest(cement_in, cement_out, fillvalue={})]

        #RSB
        rsb_in = incoming.filter(item__item_name__contains="RSB").values('item__item_name').annotate(tot_in=Sum('quantity'))
        rsb_out = incoming.filter(item__item_name__contains="RSB").values('item__item_name').annotate(tot_out=Sum('out__quantity'))
        context['rsb'] = [{**u, **v} for u, v in zip_longest(rsb_in, rsb_out, fillvalue={})]

        #Lumber
        lumber_in = incoming.filter(item__item_name__contains="Lumber").values('item__item_name').annotate(tot_in=Sum('quantity'))
        lumber_out = incoming.filter(item__item_name__contains="Lumber").values('item__item_name').annotate(tot_out=Sum('out__quantity'))
        context['lumber'] = [{**u, **v} for u, v in zip_longest(lumber_in, lumber_out, fillvalue={})]

        #Aggregates
        agg_in = incoming.filter(item__item_category="Aggregates").values('item__item_name').annotate(tot_in=Sum('quantity'))
        agg_out = incoming.filter(item__item_category="Aggregates").values('item__item_name').annotate(tot_out=Sum('out__quantity'))
        context['aggregates'] = [{**u, **v} for u, v in zip_longest(agg_in, agg_out, fillvalue={})]

        context['budiga_in'] = incoming.annotate(tot_out=Sum('out__quantity'))\
                .annotate(current_count=F('quantity')-F('tot_out'))\
                .order_by('-trans_date')[:300]
        context['budiga_out'] = outgoing.order_by('-trans_date')[:300]


        #issue tracker
        context['no_price'] = incoming.filter(unit_price=0).count()
        context['no_attach_in'] = incoming.filter(Q(attachment="") | Q(attachment=None)).count()
        context['no_attach_out'] = outgoing.filter(Q(attachment="") | Q(attachment=None)).count()
        context['x_form_in'] = incoming.exclude(form_no__regex=r'^[A-Z]*-[0-9]{2}-[0-9]*').count()
        context['x_form_out'] = outgoing.exclude(form_no__regex=r'^[A-Z]*-[0-9]{2}-[0-9]*').count()
        context['negatives'] = incoming.annotate(tot_out=Sum('out__quantity'))\
                .annotate(current_count=F('quantity')-F('tot_out'))\
                .filter(current_count__lt=0)\
                .count()


        return context


class AnalystPageView(ListView):
    model = Incoming
    template_name = 'warehouse/analyst_page.html'

    def get_context_data(self, **kwargs):
        context = super(AnalystPageView, self).get_context_data(**kwargs)

        incoming = Incoming.objects\
                .exclude(details__contains="inventory")\
                .select_related('received_by','project_site','item')

        outgoing = Outgoing.objects\
                .exclude(details__contains="inventory")\
                .select_related('project_site','released_by','released_to','released_out','unit')

        #incoming
        context['unverified_in'] = incoming.filter(status="For Verification").order_by('-trans_date')[:300]
        context['unverified_count_in'] = incoming.filter(status="For Verification").count()



        #outgoing
        context['unverified_out'] = outgoing.filter(status="For Verification").order_by('-trans_date')[:300]
        context['unverified_count_out'] = outgoing.filter(status="For Verification").count()


        return context




#Purchase Page Per Project
class DailyPurchaseView(DetailView):
    model = ProjectSite
    template_name = 'warehouse/daily_purchase_page.html'
    context_object_name = 'daily_purchase'

    def get_context_data(self, **kwargs):
        context = super(DailyPurchaseView, self).get_context_data(**kwargs)

        context['pending'] = OrderRequest.objects.filter(project_site__id=self.object.id).filter(status='For Approval')
        context['active'] = OrderRequest.objects.filter(project_site__id=self.object.id).filter(status='On-Process')
        context['liquidation'] = Liquidation.objects.filter(project_site__id=self.object.id).filter(trans_date=date.today())

        return context


#Fuel Page Per Project
class FuelView(DetailView):
    model = ProjectSite
    template_name = 'warehouse/fuel_page.html'
    context_object_name = 'fuel_per_project'

    def get_context_data(self, **kwargs):
        context = super(FuelView, self).get_context_data(**kwargs)

        transaction = Transaction.objects.filter(project_site__id=self.object.id).select_related('processed_by','tank_site','project_site','unit')

        context['incoming'] = transaction.filter(trans_type='Incoming')
        context['outgoing'] = transaction.filter(~Q(trans_type='Incoming'))

        return context


#Advance Search
def IncomingSearch(request):

    incoming = Incoming.objects\
            .select_related('received_by','project_site','item')\
            .annotate(tot_out=Sum('out__quantity'))\
            .annotate(current_count=F('quantity')-F('tot_out'))

    search_in = IncomingFilter(request.GET, queryset=incoming)

    return render(request, 'warehouse/search_in.html', {'pasok': search_in,})


def OutgoingSearch(request):
    outgoing = Outgoing.objects\
            .select_related('project_site','released_by','released_to','released_out','unit')

    search_out = OutgoingFilter(request.GET, queryset=outgoing)

    return render(request, 'warehouse/search_out.html', {'labas': search_out,})


# this will change the incoming status
def IncomingStatus(request, pk):
    in_status = Incoming.objects.get(pk=pk)
    if in_status.status == "For Verification":
        in_status.status = "Verified"
    elif in_status.status == "Verified":
        in_status.status = "For Verification"

    in_status.save()
    return HttpResponseRedirect(reverse('warehouse:sinumrek'))


# this will change the outgoing status
def OutgoingStatus(request, pk):
    out_status = Outgoing.objects.get(pk=pk)
    if out_status.status == "For Verification":
        out_status.status = "Verified"
    elif out_status.status == "Verified":
        out_status.status = "For Verification"

    out_status.save()
    return HttpResponseRedirect(reverse('warehouse:linumwar'))



class CheckerDetailView(DetailView):
    model = Incoming
    template_name = 'warehouse/checker_detail_page.html'
    context_object_name = 'warehouse_detail'

    def get_context_data(self, **kwargs):
        context = super(CheckerDetailView,self).get_context_data(**kwargs)
        context['outgoing'] = Outgoing.objects.filter(base_in=self.object)\
                .filter(trans_type='Outgoing').order_by('trans_date')
        context['transfers'] = Outgoing.objects.filter(base_in=self.object)\
                .filter(trans_type='Transfer').order_by('trans_date')

        return context


