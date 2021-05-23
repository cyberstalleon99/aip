from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models import Sum,F,Q,When,Case,DecimalField
from django.shortcuts import get_object_or_404, render

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete

from datetime import date
from django.utils import timezone

from accounting.models import (Item, ItemCode, OrderRequest, PriceList, CashBudget,
        Liquidation, Supplier, Entry, FundRequest, SubconBilling)
from workforce.models import ProjectSite, Subcon
from warehouse.models import Incoming, Outgoing
from django.db.models import Q

#test
from django.contrib.auth.models import User

from .forms import (LiquidationForm, CashBudgetForm, EntryForm, EntryForm2,
        FundRequestForm, OrderRequestForm, SubconBillingForm, SupplierForm, ItemForm)
from .filters import (PriceListFilter, PurchasedListFilter, JournalEntryFilter,
    PurchasedEntryFilter, PurchasedMonitoringFilter, CreditEntryFilter, CancelledPurchaseFilter)

# **************************************************************
# START dongilay
# **************************************************************

from warehouse.helpers import add_log, change_log

# **************************************************************
# END dongilay
# **************************************************************

# Create your views here.

current_date = timezone.now()

##############################################
# Autocompletes
##############################################
class FieldAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            # qs = qs.filter(first_name__icontains=self.q)
            qs = qs.filter(Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q))
        return qs

class CashAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CashBudget.objects.all()
        if self.q:
            qs = qs.filter(form_no__istartswith=self.q)
        return qs

class PurchaseAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = OrderRequest.objects.all()
        if self.q:
            qs = qs.filter(id__istartswith=self.q)
        return qs

class SiteAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ProjectSite.objects.all()
        if self.q:
            qs = qs.filter(project_code__icontains=self.q)
        return qs

class ItemAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Item.objects.all()
        if self.q:
            qs = qs.filter(item_name__icontains=self.q)
        return qs

class SupplierAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Supplier.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class SubconAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Subcon.objects.all()
        if self.q:
            qs = qs.filter(group_name__icontains=self.q)
        return qs

class CodeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ItemCode.objects.all()
        if self.q:
            qs = qs.filter(sc1__icontains=self.q)
        return qs

class EntryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Entry.objects.all()
        if self.q:
            qs = qs.filter(id__istartswith=self.q)
        return qs




##############################################
# Accounting Pages
##############################################
class YourEntryView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'accounting/your_entry.html'
    context_object_name = 'your_entry'

    def get_context_data(self, **kwargs):
        context = super(YourEntryView,self).get_context_data(**kwargs)
        context['unliquidated'] = Entry.objects.filter(transaction_by=self.request.user).filter(status='Unliquidated').order_by('-trans_date')
        context['all'] = Entry.objects.filter(transaction_by=self.request.user).filter(status='Liquidated').order_by('-trans_date')
        context['fund_requests'] = FundRequest.objects.filter(created_by=self.request.user).order_by('-trans_date')[:6]

        return context

class CashiersDailyView(LoginRequiredMixin, ListView ):
    model = Entry
    template_name = 'accounting/cashiers_daily.html'
    context_object_name = 'daily'

    def get_context_data(self, **kwargs):
        context = super(CashiersDailyView,self).get_context_data(**kwargs)
        entry = Entry.objects.filter(created_by=self.request.user)
        context['daily_entry'] = entry.filter(trans_date=date.today())
        context['unliquidated'] = entry.filter(status="Unliquidated")
        context['fund_requests'] = FundRequest.objects.filter(request_to=self.request.user).filter(done=False)

        return context

class ForVerificationView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'accounting/for_verification.html'

    def get_context_data(self, **kwargs):
        context = super(ForVerificationView,self).get_context_data(**kwargs)
        trans = Entry.objects.select_related('supplier','project_site','transaction_by','item','account_code','subcon','created_by','modified_by')
        context['for_verification_22'] = trans.filter(account_code__isnull=True).filter(form_no__contains="-22-")
        context['for_verification_82'] = trans.filter(account_code__isnull=True).filter(form_no__contains="-82-")
        context['for_verification_26'] = trans.filter(account_code__isnull=True).filter(form_no__contains="-26-")

        return context

def SearchJournalEntry(request):
    je = Entry.objects\
            .select_related('project_site','transaction_by','account_code','created_by','modified_by')

    search_je = JournalEntryFilter(request.GET, queryset=je)

    return render(request, 'accounting/journal_entry.html', {'je': search_je,})

# this will change status of entry to either liquidated or unliquidated
def entry_liquidated(request, pk):
    entry_status = Entry.objects.get(pk=pk)
    if entry_status.status == "Unliquidated":
        entry_status.status = "Liquidated"
    elif entry_status.status == "Liquidated":
        entry_status.status = "Unliquidated"
    entry_status.save()
    return HttpResponseRedirect(reverse('accounting:detail_entry', args=(pk,)))

class DetailEntryView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'accounting/entry_detail.html'
    context_object_name = 'entry_detail'

    def get_context_data(self, **kwargs):
        context = super(DetailEntryView,self).get_context_data(**kwargs)

        trans = Entry.objects.select_related('supplier','project_site','transaction_by','item','account_code','subcon','created_by','modified_by')
        trans_liq = trans.filter(form_no__icontains=self.object.form_no).filter(entry_type="Non-Cash").exclude(entry_credit=True)

        context['liquidations'] = trans_liq.order_by('-trans_date')

        context['cdv'] = trans\
            .filter(form_no__icontains=self.object.form_no).filter(entry_type="Non-Cash").filter(entry_credit=True)

        context['cash_return'] = trans\
            .filter(form_no__icontains=self.object.form_no).filter(account_code__item_code=4210).filter(entry_debit=True)

        context['reimbursement'] = trans\
            .filter(form_no__icontains=self.object.form_no).filter(account_code__item_code=4210).filter(entry_credit=True).filter(remarks__icontains="Reimbursement")



        context['given']= self.object.debit
        context['consumed'] = trans_liq.aggregate(liq=Sum('debit'))

        context['cluster'] = trans_liq.values('account_code__item_code').annotate(total=Sum('debit')).annotate(sc1=F('account_code__sc1')).annotate(sc2=F('account_code__sc2'))

        return context

class DetailEntryPrintView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'accounting/entry_detail_print.html'
    context_object_name = 'entry_detail'

    def get_context_data(self, **kwargs):
        context = super(DetailEntryPrintView,self).get_context_data(**kwargs)

        trans = Entry.objects.select_related('supplier','project_site','transaction_by','item','account_code','subcon','created_by','modified_by')
        trans_liq = trans.filter(form_no__icontains=self.object.form_no).filter(entry_type="Non-Cash").exclude(entry_credit=True)

        context['liquidations'] = trans_liq.order_by('-trans_date')

        context['cdv'] = trans\
            .filter(form_no__icontains=self.object.form_no).filter(entry_type="Non-Cash").filter(entry_credit=True)

        context['cash_return'] = trans\
            .filter(form_no__icontains=self.object.form_no).filter(account_code__item_code=4210).filter(entry_debit=True)

        context['reimbursement'] = trans\
            .filter(form_no__icontains=self.object.form_no).filter(account_code__item_code=4210).filter(entry_credit=True).filter(remarks__icontains="Reimbursement")



        context['given']= self.object.debit
        context['consumed'] = trans_liq.aggregate(liq=Sum('debit'))

        context['cluster'] = trans_liq.values('account_code__item_code').annotate(total=Sum('debit')).annotate(desc=F('account_code__sc1'))

        return context


##############################################
# New Entry
##############################################
class NewEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
        except:
            form.instance.created_by = None
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_entry')
        else:
            url = reverse_lazy('accounting:new_entry')

        return url

class NewEntryView2(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm2

    def get_initial(self):
        base_por = get_object_or_404(OrderRequest, pk=self.kwargs.get('pk'))
        return {'base_por':base_por,}

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
        except:
            form.instance.created_by = None
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        return reverse_lazy('accounting:detail_por', kwargs={'pk': self.object.base_por.pk})

class UpdateEntryView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['entry_list'] = Entry.objects.order_by('-created_at')[:30]
        return super(UpdateEntryView, self).get_context_data(**kwargs)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:new_entry')

class DeleteEntryView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:new_entry')


##############################################
# Fund Request
##############################################
class NewFundRequestView(CreateView):
    model = FundRequest
    form_class = FundRequestForm

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
        except:
            form.instance.created_by = None
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_entry')
        else:
            url = reverse_lazy('accounting:your_entry')

        return url

class UpdateFundRequestView(LoginRequiredMixin, UpdateView):
    model = FundRequest
    form_class = FundRequestForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:your_entry')

class DeleteFundRequestView(LoginRequiredMixin, DeleteView):
    model = FundRequest
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:new_entry')


##############################################
# Subcon Billing
##############################################
class NewBillingView(CreateView):
    model = SubconBilling
    form_class = SubconBillingForm

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
        except:
            form.instance.created_by = None
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_billing')
        else:
            url = reverse_lazy('accounting:new_billing')

        return url

class UpdateBillingView(LoginRequiredMixin, UpdateView):
    model = SubconBilling
    form_class = SubconBillingForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:new_billing')

class DeleteBillingView(LoginRequiredMixin, DeleteView):
    model = SubconBilling
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:new_billing')

class SubconBillingView(ListView):
    model = SubconBilling
    template_name = 'accounting/billing_page.html'
    context_object_name = 'billing_list'

    def get_context_data(self, **kwargs):
        context = super(SubconBillingView,self).get_context_data(**kwargs)

        context['no_retention'] = Subcon.objects.exclude(subcon=None).exclude(subcon__account_code='7700')\
            .annotate(total_bill = Sum(Case(When(subcon__account_code='2131', then=F('subcon__debit')), output_field=DecimalField(), default=0)))

        return context

# this will changee status
def StatusOPS(request, pk):
    bill_status = SubconBilling.objects.get(pk=pk)
    if bill_status.status_ops == "Open":
        bill_status.status_ops = "For-Review"
    elif bill_status.status_ops == "For-Review":
        bill_status.status_ops = "Closed"
    elif bill_status.status_ops == "Closed":
        bill_status.status_ops = "Open"

    bill_status.save()
    return HttpResponseRedirect(reverse('accounting:billing_page'))

def StatusACC(request, pk):
    bill_status = SubconBilling.objects.get(pk=pk)
    if bill_status.status_acc == "Open":
        bill_status.status_acc = "For-Review"
    elif bill_status.status_acc == "For-Review":
        bill_status.status_acc = "Closed"
    elif bill_status.status_acc == "Closed":
        bill_status.status_acc = "Open"

    bill_status.save()
    return HttpResponseRedirect(reverse('accounting:billing_page'))

def StatusWH(request, pk):
    bill_status = SubconBilling.objects.get(pk=pk)
    if bill_status.status_wh == "Open":
        bill_status.status_wh = "For-Review"
    elif bill_status.status_wh == "For-Review":
        bill_status.status_wh = "Closed"
    elif bill_status.status_wh == "Closed":
        bill_status.status_wh = "Open"

    bill_status.save()
    return HttpResponseRedirect(reverse('accounting:billing_page'))



##############################################
# Purchasing Pages
##############################################
class PendingView(ListView):
    model = OrderRequest
    template_name = 'accounting/pending_page.html'
    context_object_name = 'pending_listing'

    def get_context_data(self, **kwargs):
        context = super(PendingView,self).get_context_data(**kwargs)

        pending = OrderRequest.objects.select_related('request_by','project_site','item','purchaser').filter(Q(status__isnull = True) | Q(status = 'For Approval'))
        active = OrderRequest.objects.select_related('request_by','project_site','item','purchaser').filter(status = 'On-Process')
        invalid = OrderRequest.objects.select_related('request_by','project_site','item','purchaser').filter(status = 'Invalid')

        context['pending_count'] = pending.count()
        context['active_count'] = active.exclude(project_site__project_code = "DMHP").count()
        context['active_dmhp_count'] = active.filter(project_site__project_code = "DMHP").count()
        context['invalid_count'] = invalid.count()
        context['today_count'] = active.filter(purchaser=self.request.user).filter(today=True).count()

        context['pending_operation'] = pending.filter(item__item_category__in = ['Construction Materials','Aggregates']).order_by('-request_date')
        context['pending_equipment'] = pending.filter(item__item_category__in = ['Spare Parts','Oil & Lubricants','Tools & Machineries']).order_by('-request_date')
        context['pending_admin'] = pending.filter(item__item_category__in=['PPE','Office Supply','Food Supply','Kitchen Utensils','Fuel','IT Equipment']).order_by('-request_date')

        context['active_request'] = active.exclude(project_site__project_code = "DMHP").annotate(tot_purchased=Sum('por__quantity')).annotate(tot_entry=Sum('entry_por__quantity')).order_by('-request_date')
        context['active_dmhp'] = active.filter(project_site__project_code = "DMHP").annotate(tot_purchased=Sum('por__quantity')).annotate(tot_entry=Sum('entry_por__quantity')).order_by('-request_date')
        context['invalid_request'] = invalid.annotate(tot_purchased=Sum('por__quantity')).order_by('-request_date')

        return context

class MonitoringView(ListView):
    model = OrderRequest
    template_name = 'accounting/monitoring_page.html'

    def get_context_data(self, **kwargs):
        context = super(MonitoringView,self).get_context_data(**kwargs)

        search_purchased = OrderRequest.objects\
                .select_related('request_by','project_site','item','purchaser').annotate(actual_purchase=F('entry_por__created_at')).all()

        context['search_entry'] = PurchasedMonitoringFilter(self.request.GET, queryset=search_purchased)

        return context


class PurchasedListView(ListView):
    model = PriceList
    template_name = 'accounting/purchased_page.html'

    def get_context_data(self, **kwargs):
        context = super(PurchasedListView,self).get_context_data(**kwargs)

        search_purchased = Liquidation.objects\
                .select_related('base_budget','base_por','project_site','issued_by','item','supplier')\
                .all()

        context['search_liquidation'] = PurchasedListFilter(self.request.GET, queryset=search_purchased)

        return context

class PurchasedEntryView(ListView):
    model = OrderRequest
    template_name = 'accounting/purchased_entry.html'

    def get_context_data(self, **kwargs):
        context = super(PurchasedEntryView,self).get_context_data(**kwargs)

        search_purchased = Entry.objects\
                .exclude(item__isnull=True)

        context['search_entry'] = PurchasedEntryFilter(self.request.GET, queryset=search_purchased)

        return context

class DetailPORView(LoginRequiredMixin, DetailView):
    model = OrderRequest
    template_name = 'accounting/por_detail.html'
    context_object_name = 'por_detail'

    def get_context_data(self, **kwargs):
        context = super(DetailPORView,self).get_context_data(**kwargs)

        trans = Entry.objects.filter(base_por=self.object)
        context['liquidations'] = trans\
            .order_by('-trans_date')\
            .select_related('supplier','project_site','transaction_by','item','account_code','subcon','created_by','modified_by')

        return context

class PurchaseDetailView(DetailView):
    model = OrderRequest
    template_name = 'accounting/purchase_detail_page.html'
    context_object_name = 'purchase_detail'

    def get_context_data(self, **kwargs):
        context = super(PurchaseDetailView,self).get_context_data(**kwargs)
        context['liquidation_debit'] = Liquidation.objects.filter(base_por=self.object)\
                .select_related('base_budget','base_por','project_site','issued_by','item','supplier')\
                .order_by('trans_date')
        context['liquidation_entry'] = Entry.objects.filter(base_por=self.object)\
                .select_related('base_por','project_site','transaction_by','item','supplier','account_code','subcon')\
                .order_by('trans_date')

        #incoming from old database
        po_id = Liquidation.objects.filter(base_por=self.object).values_list('id', flat=True)
        context['incomings'] = Incoming.objects.filter(trans_no__in = list(map(str, po_id)))

        in_id = Incoming.objects.filter(trans_no__in = list(map(str, po_id))).values_list('id', flat=True)
        out = Outgoing.objects.select_related('base_in','project_site','released_by','released_to','released_out','unit')
        context['outgoings'] = out.filter(base_in__in = in_id).filter(trans_type='Outgoing')
        context['transfers'] = out.filter(base_in__in = in_id).filter(trans_type='Transfer')
        context['direct'] = out.filter(base_in__in = in_id).filter(trans_type='Direct Transfer')

        #incoming from new database
        entry_id = Entry.objects.filter(base_por=self.object).values_list('id', flat=True)
        ins = Incoming.objects.filter(trans_no__in = list(map(str, entry_id))).filter(item = self.object.item)
        context['sinumrek'] = ins

        #outgoing from new database
        ins_id = ins.values_list('id', flat=True)
        context['outgoings2'] = out.filter(base_in__in = ins_id).filter(trans_type='Outgoing')
        context['transfers2'] = out.filter(base_in__in = ins_id).filter(trans_type='Transfer')
        context['direct2'] = out.filter(base_in__in = ins_id).filter(trans_type='Direct Transfer')

        context['recent'] = Liquidation.objects\
                .filter(item = self.object.item)\
                .select_related('base_budget','base_por','project_site','issued_by','item','supplier')\
                .order_by('-trans_date')[:10]
        context['recent_new'] = Entry.objects\
                .filter(item = self.object.item)\
                .select_related('base_por','project_site','transaction_by','item','supplier','account_code','subcon')\
                .order_by('-trans_date')

        # check if it has been recorded in warehouse
        context['incoming'] = self.object.entry_por.count()
        # check if it has jo
        cat = self.object.item.item_category
        jo = self.object.jo_no
        stock = self.object.details.lower()
        que = "stock"
        if cat in ['Spare Parts','Oil & Lubricants'] and jo == None and que not in stock:
            context['needs_jo'] = {"Yes",}
        else:
            context['needs_jo'] = {"No",}

        context['sources'] = Incoming.objects.filter(item=self.object.item)\
                .select_related('received_by','project_site','item')\
                .annotate(tot_out=Sum('out__quantity'))\
                .annotate(current_count=F('quantity')-F('tot_out'))\
                .filter(current_count__gt=0)

        return context

# this will change status to on-process
def ProcessPOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    por_status.status = "On-Process"
    por_status.approved_at = timezone.now()
    por_status.save()
    return HttpResponseRedirect(reverse('accounting:pending_page'))

# this will change status to canceled
def CancelPOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    por_status.status = "Canceled"
    por_status.save()
    return HttpResponseRedirect(reverse('accounting:pending_page'))

# this will change status to invalid
def InvalidPOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    por_status.status = "Invalid"
    por_status.save()
    return HttpResponseRedirect(reverse('accounting:purchase_detail_page', args=(pk,)))

# this will change status to purchased
def ApprovePOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    if por_status.status == "On-Process":
        por_status.status = "Purchased"
        por_status.purchased_at = timezone.now()
    elif por_status.status == "Purchased":
        por_status.status = "On-Process"

    por_status.save()
    return HttpResponseRedirect(reverse('accounting:purchase_detail_page', args=(pk,)))

# this will change today status
def TodayStatus(request, pk):
    today_status = OrderRequest.objects.get(pk=pk)
    if today_status.today == False:
        today_status.today = True
    elif today_status.today == True:
        today_status.today = False

    today_status.save()
    return HttpResponseRedirect(reverse('accounting:pending_page'))


#New Credit Page
class CreditEntryView(ListView):
    model = OrderRequest
    template_name = 'accounting/utang_entry.html'

    def get_context_data(self, **kwargs):
        context = super(CreditEntryView,self).get_context_data(**kwargs)

        search_credit = Entry.objects.filter(utang=True).exclude(item__isnull=True)

        context['search_entry'] = CreditEntryFilter(self.request.GET, queryset=search_credit)

        return context


class CancelledView(ListView):
    model = OrderRequest
    template_name = 'accounting/cancelled_entry.html'

    def get_context_data(self, **kwargs):
        context = super(CancelledView,self).get_context_data(**kwargs)

        search_cancelled = OrderRequest.objects.filter(status = 'Canceled').order_by('-request_date')

        context['search_entry'] = CancelledPurchaseFilter(self.request.GET, queryset=search_cancelled)

        return context


class ItemView(ListView):
    model = Item
    template_name = 'accounting/item_list.html'
    context_object_name = 'item_list'

class PriceListView(ListView):
    model = PriceList
    template_name = 'accounting/supplier_price.html'

    def get_context_data(self, **kwargs):
        context = super(PriceListView,self).get_context_data(**kwargs)

        search_data = PriceList.objects\
                .values('supplier__name','item__item_name')\
                .annotate(price=F('price'))\
                .order_by('-price')

        search_purchased = Liquidation.objects\
                .select_related('base_budget','base_por','project_site','issued_by','item','supplier')\
                .values('supplier__name','item__item_name')\
                .annotate(price=F('amount'))\
                .annotate(quantity=F('quantity'))\
                .annotate(date=F('trans_date'))



        context['search_supplier'] = PriceListFilter(self.request.GET, queryset=search_data)
        context['search_liquidation'] = PriceListFilter(self.request.GET, queryset=search_purchased)

        return context

##############################################
# Purchase Order Request
##############################################
class NewPurchaseOrderView(LoginRequiredMixin, CreateView):
    model = OrderRequest
    form_class = OrderRequestForm

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
        except:
            form.instance.created_by = None
        return super().form_valid(form)

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_por')
        else:
            url = reverse_lazy('success')

        return url

class UpdatePurchaseOrderView(LoginRequiredMixin, UpdateView):
    model = OrderRequest
    form_class = OrderRequestForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:pending_page')

class DeletePurchaseOrderView(LoginRequiredMixin, DeleteView):
    model = OrderRequest
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:pending_page')

# **************************************************************
# START dongilay
# **************************************************************

class NewSupplierView(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'accounting/supplier_form.html'
    form_class = SupplierForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('accounting:price_list')
        return url

class UpdateSupplierView(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'accounting/supplier_form.html'
    form_class = SupplierForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:price_list')

class NewItemView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'accounting/item_form.html'
    form_class = ItemForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('accounting:item_page')
        return url

class UpdateItemView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'accounting/item_form.html'
    form_class = ItemForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:item_page')

class NewLiquidationView(LoginRequiredMixin, CreateView):
    model = Liquidation
    template_name = 'accounting/liquidation_form.html'
    form_class = LiquidationForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('accounting:pending_page')
        return url

class UpdateLiquidationView(LoginRequiredMixin, UpdateView):
    model = Liquidation
    template_name = 'accounting/liquidation_form.html'
    form_class = LiquidationForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('accounting:pending_page')

# **************************************************************
# END dongilay
# **************************************************************









