from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from bootstrap_datepicker_plus import DatePickerInput

from django.db.models import Sum, Q
from django.views.generic import DetailView, ListView, CreateView

from django.contrib.auth.models import User, Group
from operation.models import (Project, WorkStat, ProjectItem,
                            Report, AllocatedExpense, MajorExpense,
                            Billing, Reporting)
from workforce.models import EmployeeProfile
from fleet.models import UnitProfile

# Create your views here.

class IndexView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Project
    template_name = 'operation/index_page.html'
    context_object_name = 'project_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)

        context['on_going'] = Project.objects.filter(project_status='Under Construction').order_by('project_code')
        context['for_bidding'] = Project.objects.filter(project_status='For Bidding').order_by('project_code')
        context['completed'] = Project.objects.filter(project_status='Completed').order_by('project_code')

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()

class StatsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Project
    template_name = 'operation/stats_page.html'
    context_object_name = 'stats_list'

    def get_context_data(self, **kwargs):
        context = super(StatsView,self).get_context_data(**kwargs)
        context['on_going_tot'] = Project.objects.filter(project_status='Under Construction').order_by('project_code').count()
        context['on_going'] = Project.objects.filter(project_status='Under Construction').order_by('project_code')
        context['completed_tot'] = Project.objects.filter(project_status='Completed').order_by('project_code').count()
        context['completed'] = Project.objects.filter(project_status='Completed').order_by('project_code')

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'operation/detail_page.html'
    context_object_name = 'project_detail'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView,self).get_context_data(**kwargs)

        context['total_personnel'] = EmployeeProfile.objects.filter(project_site__project_code=self.object).filter(employment_status='Active').count()
        context['total_units'] = UnitProfile.objects.filter(project_site__project_code=self.object).count()

        context['aip_personnel'] = EmployeeProfile.objects.filter(project_site__project_code=self.object).filter(employment_status='Active')
        context['aip_units'] = UnitProfile.objects.filter(project_site__project_code=self.object)

        try:
            context['allocated_expense'] = AllocatedExpense.objects.filter(base_project=self.object).latest('date')
        except AllocatedExpense.DoesNotExist:
            context['allocated_expense'] = None
        try:
            context['latest_expense'] = MajorExpense.objects.filter(base_project=self.object).latest('date')
        except MajorExpense.DoesNotExist:
            context['latest_expense'] = None
        try:
            context['latest_report'] = WorkStat.objects.filter(base_project=self.object).filter(~Q(actual=0)).latest('date')
        except WorkStat.DoesNotExist:
            context['latest_report'] = None
        try:
            context['top_reports'] = Report.objects.filter(base_project=self.object).order_by('date')[:10]
        except Report.DoesNotExist:
            context['top_reports'] = None

        context['latest_billing'] = Billing.objects.filter(base_project=self.object).aggregate(bill_sum =Sum('amount'))

        try:
            reports = Reporting.objects.filter(base_project=self.object)
        except Reporting.DoesNotExist:
            context['top_reports'] = None

        context['pls'] = reports.filter(report_type = 'Project Log Sheet')
        context['swa'] = reports.filter(report_type = 'Statement of Work Accomplished')
        context['sld'] = reports.filter(report_type = 'Straight Line Diagram')
        context['geo'] = reports.filter(report_type = 'Geotagged Pictures')
        context['pm'] = reports.filter(report_type = 'Project Monitor')


        context['project_items'] = ProjectItem.objects.filter(base_project=self.object)\
                .annotate(start_year = ExtractYear('start_date'))\
                .annotate(start_month = ExtractMonth('start_date'))\
                .annotate(start_day = ExtractDay('start_date'))\
                .annotate(end_year = ExtractYear('end_date'))\
                .annotate(end_month = ExtractMonth('end_date'))\
                .annotate(end_day = ExtractDay('end_date'))\
                .order_by('start_date')

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()



