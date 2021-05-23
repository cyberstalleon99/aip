from django.urls import reverse_lazy
from django.views.generic import (ListView,CreateView,UpdateView)
from fuel.models import (Transaction, Reading, Tank)
from workforce.models import (ProjectSite,)
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete
from .forms import TransactionForm, ReadingForm, TankForm

from bootstrap_datepicker_plus import DateTimePickerInput

from django.db.models import Sum,F,Q
from .filters import FuelFilter

# **************************************************************
# START dongilay
# **************************************************************

from warehouse.helpers import add_log, change_log

# **************************************************************
# END dongilay
# **************************************************************

##############################################
# Autocompletes
##############################################

# **************************************************************
# START dongilay
# **************************************************************

class TankAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tank.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

# **************************************************************
# END dongilay
# **************************************************************

# Create your views here.
class IndexView(ListView):
    model = Transaction
    template_name = 'fuel/transaction.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)

        reports = Transaction.objects.all()
        context['search_fuel'] = FuelFilter(self.request.GET, queryset=reports)

        return context


class DashView(ListView):
    model = Transaction
    template_name = 'fuel/dash_page.html'
    context_object_name = 'dash_index'

    def get_context_data(self, **kwargs):
        context = super(DashView,self).get_context_data(**kwargs)

        fuel_trans = Transaction.objects.select_related('processed_by','tank_site','project_site','unit')

        context['all_trans'] = fuel_trans.filter(project_site__project_status='Under Construction')
        context['consumption'] = fuel_trans.filter(trans_type = 'Outgoing').values('project_site__project_code')\
                .annotate(tot_quantity=Sum(F('amount'))).order_by('-project_site__project_code')


        return context





class TransactionCreateView(CreateView):
    model = Transaction
    fields = ('trans_date','trans_type','fwf','processed_by','tank_site','project_site','unit','amount','price','remarks')
    success_url = reverse_lazy('fuel:fuel_index')

    def get_form(self):
        form = super().get_form()
        form.fields['trans_date'].widget = DateTimePickerInput()
        return form

class TransactionUpdateView(UpdateView):
    model = Transaction
    fields = ('trans_date','trans_type','fwf','processed_by','tank_site','project_site','unit','amount','price','remarks')
    success_url = reverse_lazy('fuel:fuel_index')

    def get_form(self):
        form = super().get_form()
        form.fields['trans_date'].widget = DateTimePickerInput()
        return form

class ReadingCreateView(CreateView):
    model = Reading
    fields = ('tank','read_date','conducted_by','reading')
    success_url = reverse_lazy('fuel:fuel_index')

    def get_form(self):
        form = super().get_form()
        form.fields['read_date'].widget = DateTimePickerInput()
        return form

class ReadingUpdateView(UpdateView):
    model = Reading
    fields = ('tank','read_date','conducted_by','reading')
    success_url = reverse_lazy('fuel:fuel_index')

    def get_form(self):
        form = super().get_form()
        form.fields['read_date'].widget = DateTimePickerInput()
        return form

class TankCreateView(CreateView):
    model = Tank
    fields = ('name','location','max_capacity')
    success_url = reverse_lazy('fuel:fuel_index')

class TankUpdateView(UpdateView):
    model = Tank
    fields = ('name','location','max_capacity')
    success_url = reverse_lazy('fuel:fuel_index')


# **************************************************************
# START dongilay
# **************************************************************

class NewTransactionView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'fuel/transaction_form2.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        context = super(NewTransactionView,self).get_context_data(**kwargs)

        if 'pk' in self.kwargs:
            context['project_site'] = ProjectSite.objects.get(id=self.kwargs['pk'])
        else:
            context['project_site'] = None

        return context

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'pk' in self.kwargs:
            url = reverse_lazy('warehouse:fuel_page', args=(self.kwargs['pk'],))
        else:
            url = reverse_lazy('fuel:fuel_index')
        return url

class UpdateTransactionView(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = 'fuel/transaction_form2.html'
    form_class = TransactionForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        if 'pk' in self.kwargs:
            url = reverse_lazy('warehouse:fuel_page', args=(self.kwargs['pk'],))
        else:
            url = reverse_lazy('fuel:fuel_index')
        return url

class NewReadingView(LoginRequiredMixin, CreateView):
    model = Reading
    template_name = 'fuel/reading_form2.html'
    form_class = ReadingForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'pk' in self.kwargs:
            url = reverse_lazy('warehouse:fuel_page', args=(self.kwargs['pk'],))
        else:
            url = reverse_lazy('fuel:fuel_index')
        return url

class UpdateReadingView(LoginRequiredMixin, UpdateView):
    model = Reading
    template_name = 'fuel/reading_form2.html'
    form_class = ReadingForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        if 'pk' in self.kwargs:
            url = reverse_lazy('warehouse:fuel_page', args=(self.kwargs['pk'],))
        else:
            url = reverse_lazy('fuel:fuel_index')
        return url

class NewTankView(LoginRequiredMixin, CreateView):
    model = Tank
    template_name = 'fuel/tank_form2.html'
    form_class = TankForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        if 'pk' in self.kwargs:
            url = reverse_lazy('warehouse:fuel_page', args=(self.kwargs['pk'],))
        else:
            url = reverse_lazy('fuel:fuel_index')
        return url

class UpdateTankView(LoginRequiredMixin, UpdateView):
    model = Tank
    template_name = 'fuel/tank_form2.html'
    form_class = TankForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        if 'pk' in self.kwargs:
            url = reverse_lazy('warehouse:fuel_page', args=(self.kwargs['pk'],))
        else:
            url = reverse_lazy('fuel:fuel_index')
        return url

# **************************************************************
# END dongilay
# **************************************************************




