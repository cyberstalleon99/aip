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
        Liquidation, Supplier, Entry, FundRequest)
from workforce.models import ProjectSite, Subcon
from warehouse.models import Incoming, Outgoing

#test
from django.contrib.auth.models import User

from .forms import LiquidationForm, CashBudgetForm, EntryForm, EntryForm2,FundRequestForm, OrderRequestForm
from .filters import PriceListFilter, PurchasedListFilter, JournalEntryFilter, PurchasedEntryFilter


# Create your views here.

current_date = timezone.now()

##############################################
# Autocompletes
##############################################
class FieldAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)
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
            qs = qs.filter(project_code__istartswith=self.q)
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
        context['for_verification_22'] = Entry.objects.filter(account_code__isnull=True).filter(form_no__contains="-22-")
        context['for_verification_82'] = Entry.objects.filter(account_code__isnull=True).filter(form_no__contains="-82-")
        context['for_verification_26'] = Entry.objects.filter(account_code__isnull=True).filter(form_no__contains="-26-")

        return context

def SearchJournalEntry(request):
    je = Entry.objects\
            .select_related('project_site','transaction_by','account_code','created_by','modified_by')\
            .exclude(account_code__isnull=True)

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
        return reverse_lazy('accounting:detail_por', kwargs={'pk': self.object.base_por.pk})

class UpdateEntryView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm

    def get_context_data(self, **kwargs):
        kwargs['entry_list'] = Entry.objects.order_by('-created_at')[:30]
        return super(UpdateEntryView, self).get_context_data(**kwargs)

    def get_success_url(self):
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
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_entry')
        else:
            url = reverse_lazy('accounting:your_entry')

        return url

class UpdateFundRequestView(LoginRequiredMixin, UpdateView):
    model = FundRequest
    form_class = FundRequestForm

    def get_success_url(self):
        return reverse_lazy('accounting:your_entry')

class DeleteFundRequestView(LoginRequiredMixin, DeleteView):
    model = FundRequest
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:new_entry')


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
        context['active_count'] = active.count()
        context['invalid_count'] = invalid.count()
        context['today_count'] = active.filter(purchaser=self.request.user).filter(today=True).count()

        context['pending_operation'] = pending.filter(item__item_category__in = ['Construction Materials','Aggregates']).order_by('-request_date')
        context['pending_equipment'] = pending.filter(item__item_category__in = ['Spare Parts','Oil & Lubricants','Tools & Machineries']).order_by('-request_date')
        context['pending_admin'] = pending.filter(item__item_category__in=['PPE','Office Supply','Food Supply','Kitchen Utensils','Fuel']).order_by('-request_date')

        context['active_request'] = active.annotate(tot_purchased=Sum('por__quantity')).annotate(tot_entry=Sum('entry_por__quantity')).order_by('-request_date')
        context['invalid_request'] = invalid.annotate(tot_purchased=Sum('por__quantity')).order_by('-request_date')

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

# this will changee status to on-process
def ProcessPOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    por_status.status = "On-Process"
    por_status.save()
    return HttpResponseRedirect(reverse('accounting:pending_page'))

# this will changee status to canceled
def CancelPOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    por_status.status = "Canceled"
    por_status.save()
    return HttpResponseRedirect(reverse('accounting:pending_page'))

# this will changee status to invalid
def InvalidPOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    por_status.status = "Invalid"
    por_status.save()
    return HttpResponseRedirect(reverse('accounting:purchase_detail_page', args=(pk,)))

# this will changee status to purchased
def ApprovePOR(request, pk):
    por_status = OrderRequest.objects.get(pk=pk)
    if por_status.status == "On-Process":
        por_status.status = "Purchased"
    elif por_status.status == "Purchased":
        por_status.status = "On-Process"

    por_status.save()
    return HttpResponseRedirect(reverse('accounting:purchase_detail_page', args=(pk,)))

class CreditView(ListView):
    model = OrderRequest
    template_name = 'accounting/credit_page.html'
    context_object_name = 'credit_list'

    def get_context_data(self, **kwargs):
        context = super(CreditView,self).get_context_data(**kwargs)

        context['canceled_request'] = OrderRequest.objects.filter(status = 'Canceled').order_by('-request_date')
        context['purchased_credit'] = Liquidation.objects.filter(payment='Credit').order_by('-trans_date')

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
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_por')
        else:
            url = reverse_lazy('success')

        return url

class UpdatePurchaseOrderView(LoginRequiredMixin, UpdateView):
    model = OrderRequest
    form_class = OrderRequestForm

    def get_success_url(self):
        return reverse_lazy('accounting:pending_page')

class DeletePurchaseOrderView(LoginRequiredMixin, DeleteView):
    model = OrderRequest
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:pending_page')









###############################################
# Old For Deletion
###############################################

class BranchCashierView(ListView):
    model = CashBudget
    template_name = 'accounting/bc_page.html'
    context_object_name = 'bc_list'

    def get_context_data(self, **kwargs):
        context = super(BranchCashierView,self).get_context_data(**kwargs)
        context['received'] = CashBudget.objects.filter(trans_type='Cash In').order_by('trans_date')
        context['released'] = CashBudget.objects.order_by('trans_date').filter(trans_type='Cash Out')\
                .annotate(
                    consumed=Sum(
                            Case(
                                When(Q(liquidation__trans_type='Debit'), then='liquidation__amount'),
                                output_field=DecimalField()
                                )
                            ),
                        )\
                .annotate(balance=F('amount')-F('consumed'))

        context['liquidations'] = Liquidation.objects.values('trans_date')

        return context

class BookKeeperView(ListView):
    model = CashBudget
    template_name = 'accounting/bookkeeper_page.html'
    context_object_name = 'bookkeeper_list'

    def get_context_data(self, **kwargs):
        context = super(BookKeeperView,self).get_context_data(**kwargs)
        context['for_journal'] = CashBudget.objects.filter(status='For Review', status2='For Review').order_by('trans_date')
        context['for_verification'] = CashBudget.objects.filter(status='Verified', status2='For Review').order_by('trans_date')
        context['verified'] = CashBudget.objects.filter(status='Verified', status2='Verified').order_by('trans_date')

        return context

class DailyReportView(ListView):
    model = CashBudget
    template_name = 'accounting/daily_report_page.html'
    context_object_name = 'reports_list'

    def get_context_data(self, **kwargs):
        context = super(DailyReportView, self).get_context_data(**kwargs)

        context['daily_stats'] = CashBudget.objects\
            .filter().values('trans_date').order_by('trans_date')\
            .annotate(
                in_22budget=Sum(Case(
                    When(Q(form_no__istartswith='22-') & Q(trans_type='Cash In'), then='amount'),
                    output_field=DecimalField()
                )),
                in_22return=Sum(Case(
                    When(Q(form_no__istartswith='22-') & Q(liquidation__item_code__item_code='4210'), then='liquidation__amount'),
                    output_field=DecimalField()
                )),
                out_22=Sum(Case(
                    When(Q(form_no__istartswith='22-') & Q(trans_type='Cash Out'), then='amount'),
                    output_field=DecimalField()
                )),

            )

        """
        context['daily_trans'] = CashBudget.objects\
            .filter(issued_by__username='MEA')\
            .values('trans_date').order_by('trans_date')\
            .annotate(sum=Sum('amount'))

        """
        return context

class VoucherDetailView(DetailView):
    model = CashBudget
    template_name = 'accounting/cdv_detail.html'
    context_object_name = 'cdv_detail'

    def get_context_data(self, **kwargs):
        context = super(VoucherDetailView,self).get_context_data(**kwargs)

        context['total']= CashBudget.objects.filter(pk=self.object.pk)\
            .filter(liquidation__trans_type='Debit')\
            .annotate(vatable=Sum('liquidation__vatable_sales'))\
            .annotate(vat=Sum('liquidation__incoming_vat'))\
            .annotate(tot=F('vatable')+F('vat'))\
            .annotate(bal=F('amount')-F('tot'))

        context['totals'] = Liquidation.objects.filter(base_budget=self.object)\
            .aggregate(
                total_debit=Sum(
                            Case(
                                When(Q(trans_type='Debit') | Q(trans_type='Adjustment'), then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            ),
                total_credit=Sum(
                            Case(
                                When(trans_type='Credit', then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            )
                )

        context['cdv'] = Liquidation.objects.filter(base_budget=self.object)\
            .values('item_code__item_code','item_code__sc1','item_code__sc2','item_code__sc3')\
            .order_by('item_code__item_code')\
            .annotate(
                total_debit=Sum(
                            Case(
                                When(Q(trans_type='Debit') | Q(trans_type='Adjustment'), then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            ),
                total_vat=Sum(
                            Case(
                                When(Q(trans_type='Debit') | Q(trans_type='Adjustment'), then='incoming_vat'),
                                output_field=DecimalField()
                                )
                            ),
                total_credit=Sum(
                            Case(
                                When(trans_type='Credit', then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            )
                )

        return context

class IndexView(ListView):
    model = CashBudget
    template_name = 'accounting/index_page.html'
    context_object_name = 'accounting_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['unliquidated'] = CashBudget.objects.filter(status='Unliquidated', status2='For Review')\
                    .order_by('-trans_date')\
                    .annotate(
                        consumed=Sum(
                                Case(
                                    When(Q(liquidation__trans_type='Debit'), then='liquidation__amount'),
                                    output_field=DecimalField()
                                    )
                                ),
                            )\
                    .annotate(balance=F('amount')-F('consumed'))

        context['all'] = CashBudget.objects.order_by('-trans_date')\
                    .annotate(
                        consumed=Sum(
                                Case(
                                    When(Q(liquidation__trans_type='Debit'), then='liquidation__amount'),
                                    output_field=DecimalField()
                                    )
                                ),
                            )\
                    .annotate(balance=F('amount')-F('consumed'))

        return context

#cash budget form - for cashiers daily page
class NewCashBudgetView(LoginRequiredMixin, CreateView):
    model = CashBudget
    form_class = CashBudgetForm

    def get_context_data(self, **kwargs):
        context = super(NewCashBudgetView,self).get_context_data(**kwargs)

        transaction = CashBudget.objects.filter(trans_date=current_date)
        context['cash_in_today'] = transaction.filter(issued_to=self.request.user).filter(trans_type = 'Cash In').order_by('-create_date')
        context['cash_out_today'] = transaction.filter(issued_by=self.request.user).filter(trans_type = 'Cash Out').order_by('-create_date')

        context['cash_in_total'] = transaction.filter(issued_to=self.request.user).filter(trans_type = 'Cash In').order_by('-create_date').aggregate(tots=Sum('amount'))
        context['cash_out_total'] = transaction.filter(issued_by=self.request.user).filter(trans_type = 'Cash Out').order_by('-create_date').aggregate(tots=Sum('amount'))

        return context

    def get_initial(self):
        issued_by = self.request.user
        return {'issued_by':issued_by,}

    def get_success_url(self):
        return reverse_lazy('accounting:new_cashbudget')

class UpdateCashBudgetView(LoginRequiredMixin, UpdateView):
    model = CashBudget
    form_class = CashBudgetForm

    def get_context_data(self, **kwargs):
        context = super(UpdateCashBudgetView,self).get_context_data(**kwargs)

        transaction = CashBudget.objects.filter(trans_date=current_date)
        context['cash_in_today'] = transaction.filter(issued_to=self.request.user).filter(trans_type = 'Cash In').order_by('-create_date')
        context['cash_out_today'] = transaction.filter(issued_by=self.request.user).filter(trans_type = 'Cash Out').order_by('-create_date')

        context['cash_in_total'] = transaction.filter(issued_to=self.request.user).filter(trans_type = 'Cash In').order_by('-create_date').aggregate(tots=Sum('amount'))
        context['cash_out_total'] = transaction.filter(issued_by=self.request.user).filter(trans_type = 'Cash Out').order_by('-create_date').aggregate(tots=Sum('amount'))

        return context

    def get_success_url(self):
        return reverse_lazy('accounting:new_cashbudget')

class LiquidationDetailView(DetailView):
    model = CashBudget
    template_name = 'accounting/liquidation_detail.html'
    context_object_name = 'liquidation_detail'

    def get_context_data(self, **kwargs):
        context = super(LiquidationDetailView,self).get_context_data(**kwargs)

        liq = Liquidation.objects.filter(base_budget=self.object)
        context['liquidation_debit'] = liq\
                .filter(trans_type='Debit').order_by('-trans_date')\
                .select_related('base_budget','base_por','project_site','issued_by','item','supplier')

        context['total']= CashBudget.objects.filter(pk=self.object.pk)\
            .filter(liquidation__trans_type='Debit')\
            .select_related('issued_by','issued_to')\
            .annotate(vatable=Sum('liquidation__vatable_sales'))\
            .annotate(vat=Sum('liquidation__incoming_vat'))\
            .annotate(tot=F('vatable')+F('vat'))\
            .annotate(bal=F('amount')-F('tot'))

        context['totals'] = liq\
            .select_related('base_budget','base_por','project_site','issued_by','item','supplier')\
            .aggregate(
                total_debit=Sum(
                            Case(
                                When(Q(trans_type='Debit') | Q(trans_type='Adjustment'), then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            ),
                total_credit=Sum(
                            Case(
                                When(trans_type='Credit', then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            )
                )

        return context

class LiquidationPrintView(DetailView):
    model = CashBudget
    template_name = 'accounting/liquidation_print.html'
    context_object_name = 'liquidation_detail'

    def get_context_data(self, **kwargs):
        context = super(LiquidationPrintView,self).get_context_data(**kwargs)

        liq = Liquidation.objects.filter(base_budget=self.object)
        context['liquidation_debit'] = liq\
                .filter(trans_type='Debit').order_by('-trans_date')\
                .select_related('base_budget','base_por','project_site','issued_by','item','supplier')

        context['total']= CashBudget.objects.filter(pk=self.object.pk)\
            .filter(liquidation__trans_type='Debit')\
            .select_related('issued_by','issued_to')\
            .annotate(vatable=Sum('liquidation__vatable_sales'))\
            .annotate(vat=Sum('liquidation__incoming_vat'))\
            .annotate(tot=F('vatable')+F('vat'))\
            .annotate(bal=F('amount')-F('tot'))

        context['totals'] = liq\
            .select_related('base_budget','base_por','project_site','issued_by','item','supplier')\
            .aggregate(
                total_debit=Sum(
                            Case(
                                When(Q(trans_type='Debit') | Q(trans_type='Adjustment'), then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            ),
                total_credit=Sum(
                            Case(
                                When(trans_type='Credit', then='vatable_sales'),
                                output_field=DecimalField()
                                )
                            )
                )

        return context

class NewLiquidationView(LoginRequiredMixin, CreateView):
    model = Liquidation
    form_class = LiquidationForm

    def get_initial(self):
        base_budget = get_object_or_404(CashBudget, pk=self.kwargs.get('pk'))
        issued_by = self.request.user
        return {'base_budget':base_budget, 'issued_by':issued_by,}

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            url = reverse_lazy('accounting:new_liquidation', kwargs={'pk': self.object.base_budget.pk})
        else:
            url = reverse_lazy('accounting:ca_detail', kwargs={'pk': self.object.base_budget.pk})

        return url

class UpdateLiquidationView(LoginRequiredMixin, UpdateView):
    model = Liquidation
    form_class = LiquidationForm

    def get_success_url(self):
        return reverse_lazy('accounting:ca_detail', kwargs={'pk': self.object.base_budget.pk})

class DeleteLiquidationView(LoginRequiredMixin, DeleteView):
    model = Liquidation
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('accounting:ca_detail', kwargs={'pk': self.object.base_budget.pk})




















