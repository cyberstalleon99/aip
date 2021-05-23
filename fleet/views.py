import csv, io
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from dal import autocomplete
from django.db.models import Q

from django.views.generic import DetailView, ListView, CreateView, UpdateView
#new libraries


from django.views.generic import DetailView, ListView
from django.db.models import Count,When,Case,IntegerField,DecimalField,Sum,F,Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from fleet.models import (UnitProfile, JobOrder, WorkOrder, Attachment,
        Delivery, UtilizationReport, UtilizationReport, Travel)
from fuel.models import Transaction
from workforce.models import EmployeeProfile, ProjectSite
from warehouse.models import Outgoing
from accounting.models import OrderRequest
from .forms import TravelForm, UpdateTravelForm
from .filters import TravelFilter, WorkOrderFilter, URFilter

from .aip_sms_sender import TravelSms

import datetime

# **************************************************************
# START dongilay
# **************************************************************

from warehouse.helpers import add_log, change_log

# **************************************************************
# END dongilay
# **************************************************************

today = datetime.datetime.now()

##############################################
# Autocompletes
##############################################
class UnitAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = UnitProfile.objects.all()
        if self.q:
            qs = qs.filter(body_no__icontains=self.q)
        return qs

# Create your views here.
class DashView(ListView):
    model = UnitProfile
    template_name = 'fleet/dash_page.html'

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)

        base_units = UnitProfile.objects.all()

        context['all_units'] = base_units.order_by('body_no').exclude(unit_type='Uncategorized')
        context['all_tools_and_mach'] = base_units.filter(unit_type='Uncategorized')
        context['total_units'] = base_units.count()
        context['total_operational'] = base_units.filter(status='Operational').count()
        context['total_idle'] = base_units.filter(status='Idle').count()
        context['total_repair'] = base_units.filter(status='Under Repair').count()
        context['total_pms'] = JobOrder.objects.filter(status='For PMS').count()
        context['total_disposal'] = base_units.filter(status='For Disposal').count()

        base_employee = EmployeeProfile.objects.filter(employment_status='Active')

        context['total_drivers'] = base_employee.filter(designation__icontains ='Driver').count()
        context['total_operators'] = base_employee.filter(designation__icontains ='Operator').count()
        context['total_mechanics'] = base_employee.filter(designation__icontains ='Mechanic').count()
        context['total_helpers'] = base_employee.filter(designation__icontains ='Helper').count()

        base_jo = JobOrder.objects.filter(status = 'For Approval')
        base_wo = WorkOrder.objects.filter(wo_status='Under Repair')

        context['total_jo'] = base_jo.count()
        context['total_wo'] = base_wo.count()

        context['job_orders'] = base_jo.order_by('-request_date')
        context['under_repair'] = base_wo.order_by('-date_start')

        pending = OrderRequest.objects.filter(Q(status__isnull = True) | Q(status = 'For Approval'))
        context['spare_parts'] = pending.filter(item__item_category = 'Spare Parts').count()
        context['lubricants'] = pending.filter(item__item_category = 'Oil & Lubricants').count()
        context['tools'] = pending.filter(item__item_category = 'Tools & Machineries').count()


        #for the unit dashboard
        context['mechanics'] = base_employee.filter(designation__icontains ='Mechanic')
        context['unit_type'] = base_units.values('unit_type').distinct().order_by('unit_type')
        context['project_site'] = ProjectSite.objects.filter(project_status='Under Construction').values('project_code')\
                .distinct().order_by('project_code')

        context['units'] = base_units.values('project_site__project_code','unit_type')\
                .annotate(
                    operational=Count(Case(
                        When(status='Operational', then=1),
                        output_field=IntegerField(),
                    ))
                )\
                .annotate(
                    under_repair=Count(Case(
                        When(status='Under Repair', then=1),
                        output_field=IntegerField(),
                    ))
                )\
                .annotate(
                    for_disposal=Count(Case(
                        When(status='For Disposal', then=1),
                        output_field=IntegerField(),
                    ))
                )

        return context


class StatView(ListView):
    model = UnitProfile
    template_name = 'fleet/stat_page.html'
    context_object_name = 'fleet_stat'

    def get_context_data(self, **kwargs):
        context = super(StatView,self).get_context_data(**kwargs)

        context['units'] = UnitProfile.objects.annotate(wo=Count('repair_unit__work_order')).order_by('-wo')
        context['materials_used'] = Outgoing.objects.filter(trans_type='Outgoing')\
                .filter(~Q(unit = None)).values('unit__body_no')\
                .annotate(material_count=Count('create_date'))\
                .annotate(est_cost=Sum(F('quantity')*F('base_in__unit_price'))).order_by('-est_cost')
        context['fuel_used'] = Transaction.objects.filter(trans_type='Outgoing')\
                .values('unit__body_no')\
                .annotate(fuel_amount=Sum('amount'))\
                .annotate(fuel_cost=Sum(F('amount')*F('price'))).order_by('-fuel_amount')
        context['work_stat'] = WorkOrder.objects.filter(date_start__year=today.year)\
                .annotate(date=TruncMonth('date_start')).values('date')\
                .annotate(total_count=Count('date_start')).order_by('date')
        context['work_end'] = WorkOrder.objects.filter(date_end__year=today.year)\
                .annotate(date=TruncMonth('date_end')).values('date')\
                .annotate(total_count=Count('date_end')).order_by('date')
        context['top_materials'] = Outgoing.objects.filter(trans_type='Outgoing').filter(~Q(unit = None))\
                .values('base_in__item__item_name').annotate(total_count=Count('create_date'))\
                .annotate(total_sum=Sum(F('quantity')*F('base_in__unit_price'))).order_by('-total_count')[:10]
        context['cause_of_repair'] = WorkOrder.objects.filter(date_start__year=today.year)\
                .values('repair_cause').annotate(total_count=Count('create_date')).order_by('-total_count')

        return context


class WorkOrderView(ListView):
    model = WorkOrder
    template_name = 'fleet/wo.html'
    context_object_name = 'wo_index'

    def get_context_data(self, **kwargs):
        context = super(WorkOrderView, self).get_context_data(**kwargs)

        base_jo = JobOrder.objects.filter(status = 'For Approval')

        context['jo_count'] = base_jo.count()
        context['job_orders'] = base_jo.order_by('-request_date')

        under_repair = WorkOrder.objects.filter(wo_status = 'Under Repair')
        sustained = WorkOrder.objects.filter(base_jo__status = 'Sustained').filter(wo_status = 'Sustained')

        context['scheduled_count'] = under_repair.filter(service_type = 'Scheduled').count()
        context['unscheduled_count'] = under_repair.filter(service_type = 'Unscheduled').count()
        context['capital_count'] = under_repair.filter(service_type = 'Capital Repair').count()
        context['pms_count'] = WorkOrder.objects.filter(wo_status = 'For PMS').filter(service_type = 'PMS').count()

        context['sustained_count'] = sustained.count()

        context['scheduled'] = under_repair.filter(service_type = 'Scheduled').order_by('-date_start')
        context['unscheduled'] = under_repair.filter(service_type = 'Unscheduled').order_by('-date_start')
        context['capital_repair'] = under_repair.filter(service_type = 'Capital Repair').order_by('-date_start')
        context['pms'] = WorkOrder.objects.filter(wo_status = 'For PMS').filter(service_type = 'PMS').order_by('-date_start')

        context['sustained'] = sustained.order_by('-date_start')

        return context

class WorkOrderSearchView(ListView):
    model = WorkOrder
    template_name = 'fleet/wo_all.html'
    context_object_name = 'wo_search'

    def get_queryset(self):

        wo = WorkOrder.objects.all()
        search_in = WorkOrderFilter(self.request.GET, queryset=wo)
        return search_in


class UnitMapView(ListView):
    model = UnitProfile
    template_name = 'fleet/unit_map.html'
    context_object_name = 'unit_map'

    def get_context_data(self, **kwargs):
        context = super(UnitMapView,self).get_context_data(**kwargs)

        context['main'] = ProjectSite.objects.filter(project_type='Warehouse').filter(project_status='Under Construction')
        context['sites'] = ProjectSite.objects.filter(project_type='Project').filter(project_status='Under Construction')
        context['he'] = UnitProfile.objects.filter(unit_type='HE')
        context['dt'] = UnitProfile.objects.filter(unit_type='DT')
        context['units'] = UnitProfile.objects.values('unit_type').order_by('-status')

        return context


class CalendarView(ListView):
    model = Attachment
    template_name = 'fleet/calendar.html'
    context_object_name = 'calendar_index'

    def get_context_data(self, **kwargs):
        context = super(CalendarView,self).get_context_data(**kwargs)

        context['for_renewal'] = Attachment.objects.filter(expiry_date__lte=datetime.date.today())

        return context


class GalleryView(ListView):
    model = UnitProfile
    template_name = 'fleet/gallery_page.html'
    context_object_name = 'fleet_gallery'

    def get_context_data(self, **kwargs):
        context = super(GalleryView,self).get_context_data(**kwargs)

        context['units'] = UnitProfile.objects.order_by('body_no')

        return context


class UnitDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UnitProfile
    template_name = 'fleet/detail_page.html'
    context_object_name = 'unit_detail'

    def get_context_data(self, **kwargs):
        context = super(UnitDetailView,self).get_context_data(**kwargs)

        context['units'] = UnitProfile.objects.order_by('body_no')
        context['fuel'] = Transaction.objects.filter(trans_type='Outgoing').filter(unit=self.object)
        try:
            context['latest_fuel'] = Transaction.objects.filter(trans_type='Outgoing').filter(unit=self.object).latest('trans_date')
        except:
            context['latest_fuel'] = ""

        context['materials_used'] = Outgoing.objects.filter(unit=self.object).filter(Q(trans_type='Outgoing') | Q(trans_type='Direct Transfer')).order_by('-trans_date')
        context['tools_issued'] = Outgoing.objects.filter(unit=self.object).filter(Q(trans_type='Outgoing') | Q(trans_type='Direct Transfer')).filter(base_in__item__item_category='Tools & Machineries').order_by('-trans_date')
        context['materials_count'] = Outgoing.objects.filter(unit=self.object).filter(trans_type='Outgoing')\
            .values('unit__body_no')\
            .annotate(est_count=Count('create_date'))\
            .annotate(est_cost=Sum(F('quantity')*F('base_in__unit_price')))
        context['fuel_used'] = Transaction.objects.filter(unit=self.object).filter(trans_type='Outgoing')\
                .values('unit__body_no')\
                .annotate(fuel_amount=Sum('amount'))\
                .annotate(fuel_cost=Sum(F('amount')*F('price')))

        context['ur'] = UtilizationReport.objects.filter(unit_id=self.object)

        context['months'] = ('Jan','February','March','April','May','June','July','August','September','October','November','December')
        context['num_months'] = (1,2,3,4,5,6,7,8,9,10,11,12)


        materials = Outgoing.objects.filter(unit=self.object).filter(trans_type='Outgoing').filter(trans_date__year=today.year)
        context['tire_recap'] = materials.filter(base_in__item__general_name='Tire Recap')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['tire_flap'] = materials.filter(base_in__item__general_name='Tire Flap')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['tire_interior'] = materials.filter(base_in__item__general_name='Tire Interior')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['tire_bn'] = materials.filter(base_in__item__general_name='Tire B/N')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['tire_bp'] = materials.filter(base_in__item__general_name='Brake Pad')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')

        context['hydraulic_oil'] = materials.filter(base_in__item__general_name='Hydraulic Oil')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['engine_oil'] = materials.filter(base_in__item__general_name='Engine Oil')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['brake_fluid'] = materials.filter(base_in__item__general_name='Brake Fluid')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')
        context['coolant'] = materials.filter(base_in__item__general_name='Radiator Coolant')\
                .annotate(month=TruncMonth('trans_date')).values('month','base_in__item__general_name')\
                .annotate(total_count=Sum('quantity')).order_by('month')

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Fleet').exists()


class JoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = JobOrder
    template_name = 'fleet/jo_detail_page.html'
    context_object_name = 'jo_detail'

    def get_context_data(self, **kwargs):
        context = super(JoDetailView,self).get_context_data(**kwargs)

        context['wo'] = WorkOrder.objects.filter(base_jo=self.object).order_by('-date_start')

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Fleet').exists()


class DeliveryView(ListView):
    model = Delivery
    template_name = 'fleet/aip_padala.html'
    context_object_name = 'padala_list'

    def get_context_data(self, **kwargs):
        context = super(DeliveryView,self).get_context_data(**kwargs)

        delivery = Delivery.objects.all()

        context['active'] = delivery.exclude(status='Received').order_by('-create_date')
        context['confirmed'] = delivery.filter(status='Received').order_by('-create_date')

        context['stats'] = delivery.filter(status='Received')\
            .values('source__project_code','destination__project_code')\
            .annotate(frequency=Count('status'))

        return context


class DeliveryMirrorView(ListView):
    model = Delivery
    template_name = 'base_mirror.html'
    context_object_name = 'padala_list'

    def get_context_data(self, **kwargs):
        context = super(DeliveryMirrorView,self).get_context_data(**kwargs)

        delivery = Delivery.objects.all()

        context['active'] = delivery.exclude(status='Received').order_by('-create_date')
        context['confirmed'] = delivery.filter(status='Received').order_by('-create_date')

        context['stats'] = delivery.filter(status='Received')\
            .values('source__project_code','destination__project_code')\
            .annotate(frequency=Count('status'))

        return context

class TravelSearchView(ListView):
    model = Travel
    template_name = 'fleet/all_travels.html'
    context_object_name = 'all_travels'

    def get_queryset(self):

        travels = Travel.objects.order_by('-create_date')
        search_in = TravelFilter(self.request.GET, queryset=travels)
        return search_in

    # def get_context_data(self, **kwargs):
    #     context = super(TravelSearchView,self).get_context_data(**kwargs)

    #     travels = Travel.objects.order_by('-create_date')
    #     search_in = TravelFilter(self.request.GET, queryset=travels)
    #     context['travels'] = search_in
    #     return context


class TravelView(ListView):
    model = Travel
    template_name = 'fleet/travel.html'
    context_object_name = 'travel_history'

    def get_context_data(self, **kwargs):
        context = super(TravelView,self).get_context_data(**kwargs)

        travel = Travel.objects.all()

        context['today'] = travel.filter(date_start=datetime.date.today())
        # context['today'] = travel.filter(date_start=datetime.date.today()) \
        #                     .exclude(status='For Approval').exclude(status='Returned') \
        #                     .exclude(status='Canceled') \
        #                     .exclude(status='Arrived', trip='One Way')
        date_ystrdy = today - datetime.timedelta(days=1)

        context['upcoming'] = travel.filter(date_start__gt=datetime.date.today())
        context['for_approval'] = travel.filter(status='For Approval')
        # context['pending'] = travel.filter(date_start__lte=date_ystrdy) \
        #                     .exclude(status='Scheduled') \
        #                     .exclude(status='Canceled') \
        #                     .exclude(status='Returned') \
        #                     .exclude(status='For Approval') \
        #                     .exclude(status='Arrived', trip='One Way') \
        #                     .order_by('date_start')
        context['pending'] = travel.filter(date_start__lt=datetime.date.today()) \
                            .exclude(Q(status='Scheduled') | Q(status='Canceled') | Q(status='Returned') | Q(status='For Approval')) \
                            .exclude(status='Arrived', trip='One Way') \
                            .order_by('date_start')
        context['padala'] = Delivery.objects.filter(status__in = ['For Pick-Up','Processing'])

        return context

def TravelStatus(request, pk):
    travel_status = Travel.objects.get(pk=pk)

    if travel_status.status == "Travel Booked":
        travel_status.status = "On its way"
        travel_status.started_at = datetime.datetime.now()
    elif travel_status.status == "On its way":
        travel_status.status = "Arrived"
        travel_status.arrived_at = datetime.datetime.now()
    elif travel_status.status == "Arrived":
        travel_status.status = "Coming back"
        travel_status.returning_at = datetime.datetime.now()
    elif travel_status.status == "Coming back":
        travel_status.status = "Returned"
        travel_status.returned_at = datetime.datetime.now()
    elif travel_status.status == "Returned":
        travel_status.status = "Canceled"

    travel_status.save()
    return HttpResponseRedirect(reverse('fleet:travel_page'))


class UtilizationReportView(ListView):
    model = UtilizationReport
    template_name = 'fleet/ur_page.html'

    def get_context_data(self, **kwargs):
        context = super(UtilizationReportView,self).get_context_data(**kwargs)

        reports = UtilizationReport.objects.all()

        context['search_ur'] = URFilter(self.request.GET, queryset=reports)

        #context['project_sites'] = reports.values('project_site').distinct().order_by('project_site')
        context['project_sites'] = ProjectSite.objects\
                .filter(project_status='Under Construction')\
                .filter(project_type__icontains='Project')

        context['per_type'] = reports.values('project_site','unit_type')\
            .filter(unit_type__in = ['Forward-DT','Mini-DT','10 Wheeler-DT','Backhoe','Crawler'])\
                .annotate(
                    gravel_l=Sum(Case(
                        When(material='Gravel', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    base_course_l=Sum(Case(
                        When(material='Base Course', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    rough_sand_l=Sum(Case(
                        When(material='Rough Sand', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    fine_sand_l=Sum(Case(
                        When(material='Fine Sand', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    boulders_l=Sum(Case(
                        When(material='Boulders', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    excavation_l=Sum(Case(
                        When(activity='Excavation', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    gravel_h=Sum(Case(
                        When(material='Gravel', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    base_course_h=Sum(Case(
                        When(material='Base Course', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    rough_sand_h=Sum(Case(
                        When(material='Rough Sand', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    fine_sand_h=Sum(Case(
                        When(material='Fine Sand', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    boulders_h=Sum(Case(
                        When(material='Boulders', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    excavation_h=Sum(Case(
                        When(activity='Excavation', then='twh'),
                        output_field=DecimalField(),
                    ))
                )

        context['per_site'] = reports.values('project_site')\
            .filter(unit_type__in = ['Forward-DT','Mini-DT','10 Wheeler-DT','Backhoe','Crawler'])\
                .annotate(
                    gravel_l=Sum(Case(
                        When(material='Gravel', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    base_course_l=Sum(Case(
                        When(material='Base Course', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    rough_sand_l=Sum(Case(
                        When(material='Rough Sand', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    fine_sand_l=Sum(Case(
                        When(material='Fine Sand', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    boulders_l=Sum(Case(
                        When(material='Boulders', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    excavation_l=Sum(Case(
                        When(activity='Excavation', then='load'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    gravel_h=Sum(Case(
                        When(material='Gravel', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    base_course_h=Sum(Case(
                        When(material='Base Course', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    rough_sand_h=Sum(Case(
                        When(material='Rough Sand', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    fine_sand_h=Sum(Case(
                        When(material='Fine Sand', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    boulders_h=Sum(Case(
                        When(material='Boulders', then='twh'),
                        output_field=DecimalField(),
                    ))
                )\
                .annotate(
                    excavation_h=Sum(Case(
                        When(activity='Excavation', then='twh'),
                        output_field=DecimalField(),
                    ))
                )

        #Issue Tracking
        context['no_site'] = reports.filter(project_site='').count()
        context['no_unit'] = reports.filter(unit_id='').count()
        context['no_load'] = reports.exclude(material='').filter(load=0).count()

        return context


def ur_upload(request):
    template = "fleet/ur_upload.html"

    prompt = {
        'order': 'Make sure your csv file is formatted properly'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = UtilizationReport.objects.update_or_create(
            date = column[0],
            employee_id = column[1],
            unit_id = column[2],
            smr_start = column[3],
            smr_end = column[4],
            kmr_start = column[5],
            kmr_end = column[6],
            remarks = column[7],
            project_site = column[8],
            start_hour = column[9],
            end_hour = column[10],
            twh = column[16],
            activity = column[11],
            material = column[12],
            load = column[13],
            operator = column[14],
            unit_type = column[15]

        )
    context = {}
    return render(request, template, context)

# **************************************************************
# START dongilay
# **************************************************************

class NewTravelView(LoginRequiredMixin, CreateView):
    model = Travel
    template_name = 'fleet/travel_form.html'
    form_class = TravelForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)

        if self.object.status == "For Approval":
            message = TravelSms(self)
            message.send_new()

        return reverse_lazy('fleet:travel_page')

class UpdateTravelView(LoginRequiredMixin, UpdateView):
    model = Travel
    template_name = 'fleet/travel_form.html'
    form_class = UpdateTravelForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)

        if self.object.status == "Travel Booked":
            message = TravelSms(self)
            message.send_update()

        return reverse_lazy('fleet:travel_page')

# **************************************************************
# END dongilay
# **************************************************************



