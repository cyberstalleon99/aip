from django.db.models import (Sum, Count, Case, When, IntegerField, Q, F, DecimalField)
from datetime import date
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from django.template import Context
from dal import autocomplete
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import DetailView, ListView, CreateView, UpdateView
from workforce.models import (BasicProfile, ProjectSite, WorkHistory, Leave, Loans,
    Payment, FileDocument, Attachment, Outsider, Subcon)
from django.contrib.auth.models import User

from .forms import LeaveForm, UpdateLeaveForm, SuperLeaveForm, AdminLeaveForm, OutsiderForm, SubconForm, FileDocumentForm
from warehouse.helpers import add_log, change_log

from django.contrib.admin.models import LogEntry
from .filters import LogFilter
from django.shortcuts import render

from .aip_leave_sms import LeaveSMS
from .aip_mailer import AIPLeaveMailer

current_date = timezone.now()

##############################################
# Autocompletes
##############################################

# **************************************************************
# START dongilay
# **************************************************************
# mailer = AIPLeaveMailer

class OutsiderAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Outsider.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class BasicProfileAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = BasicProfile.objects.all()
        if self.q:
            qs = qs.filter(fname__icontains=self.q)
        return qs

# **************************************************************
# END dongilay
# **************************************************************

class NotificationsView(ListView):
    model = FileDocument
    template_name = 'workforce/notifications_page.html'
    context_object_name = 'renewal_list'

    def get_context_data(self, **kwargs):
        context = super(NotificationsView,self).get_context_data(**kwargs)

        context['for_renewal'] = FileDocument.objects.filter(expiry_date__lte=date.today())

        return context


# Create your views here.
class IndexView(ListView):
    model = BasicProfile
    template_name = 'workforce/index_page.html'
    context_object_name = 'profile_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)

        active_employees = BasicProfile.objects.filter(employee_profile__employment_status='Active')

        context['profiles'] = active_employees.select_related('employee_profile').order_by('-employee_profile__date_hired')

        context['total_workforce'] = active_employees.count()
        context['total_baguio'] = active_employees.select_related('employee_profile').filter(employee_profile__branch='Baguio').count()
        context['total_bontoc'] = active_employees.select_related('employee_profile').filter(employee_profile__branch='Bontoc').count()
        context['total_tagaytay'] = active_employees.select_related('employee_profile').filter(employee_profile__branch='Tagaytay').count()

        context['total_nosss'] = active_employees.count() - active_employees.select_related('accounts').filter(accounts__title='SSS').count()
        context['total_nophic'] = active_employees.count() - active_employees.select_related('accounts').filter(accounts__title='PHIC').count()
        context['total_notin'] = active_employees.count() - active_employees.select_related('accounts').filter(accounts__title='TIN').count()
        context['total_nothdmf'] = active_employees.count() - active_employees.select_related('accounts').filter(accounts__title='HDMF').count()

        context['site_total_workers'] = ProjectSite.objects.values('project_code').filter(project_status='Under Construction').annotate(
            total_workers = Count(
                Case(
                    When(Q(site__employment_status='Active') & Q(project_status='Under Construction'), then=1), output_field=IntegerField(),))
            ).order_by('project_code')

        context['bday_celeb'] = active_employees.filter(dbirth__month = date.today().month).order_by('dbirth')
        context['latest_members'] = active_employees.select_related('employee_profile').order_by('-employee_profile__date_hired')[:10]

        #Check for Documents for Renewal
        expired = FileDocument.objects.filter(expiry_date = date.today()).filter(status = 'Renewed')
        for document in expired:
            subject = 'Document for renewal: ' + str(document.document_title)
            message = 'Click the link below for details! Link: https://eakdev.pythonanywhere.com/workforce/file/'
            send_mail(
                subject,
                message,
                'aip911dispatch@gmail.com',
                ['erickiser87@gmail.com',],
                fail_silently=False,
            )
            document.status = 'Documents'
            document.save()


        return context


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BasicProfile
    template_name = 'workforce/detail_page.html'
    context_object_name = 'profile_detail'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView,self).get_context_data(**kwargs)
        context['leave_stat'] = Leave.objects.filter(base_profile=self.object)\
                .filter(date_to__year = current_date.year)\
                .aggregate(
                    all_leave=Sum('tots_days'),
                    vacation=Sum(
                            Case(
                                When(Q(leave_type='Vacation Leave'), then='tots_days'),
                                output_field=DecimalField()
                                )
                            ),
                    sick=Sum(
                            Case(
                                When(Q(leave_type='Sick Leave'), then='tots_days'),
                                output_field=DecimalField()
                                )
                            ),
                    others=Sum(
                            Case(
                                When(~Q(leave_type='Vacation Leave') & ~Q(leave_type='Sick Leave'), then='tots_days'),
                                output_field=DecimalField()
                                )
                            ),
                    with_pay=Sum(
                            Case(
                                When(Q(approval='Approved w/ Pay'), then='tots_days'),
                                output_field=DecimalField()
                                )
                            ),
                    without=Sum(
                            Case(
                                When(Q(approval='Approved w/o Pay'), then='tots_days'),
                                output_field=DecimalField()
                                )
                            )
                    )

        context['loan_stat'] = Loans.objects.filter(base_profile=self.object)\
                                    .annotate(payed=Sum('loan_payment__amount'))\
                                    .annotate(balance=F('amount')-F('payed'))\
                                    .order_by('trans_date')

        attachment = Attachment.objects.filter(base_profile=self.object)
        context['memo'] = attachment.filter(document_type__in=['Memo','Warning','Notice to Explain'])
        context['certificates'] = attachment.filter(document_type__in=['Certificate','License'])
        context['evaluations'] = attachment.filter(document_type__in=['Performance Evaluation','EDS'])
        context['others'] = attachment.filter(document_type__in=['Others',])

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Workforce').exists()


class BenefitsView(ListView):
    model = BasicProfile
    template_name = 'workforce/benefit_page.html'
    context_object_name = 'benefits_list'

    def get_context_data(self, **kwargs):
        context = super(BenefitsView,self).get_context_data(**kwargs)

        active_employees = BasicProfile.objects.filter(employee_profile__employment_status='Active')

        context['nosss'] = active_employees.filter(~Q(accounts__title='SSS'))
        context['nophic'] = active_employees.filter(~Q(accounts__title='PHIC'))
        context['notin'] = active_employees.filter(~Q(accounts__title='TIN'))
        context['nohdmf'] = active_employees.filter(~Q(accounts__title='HDMF'))

        context['work_history'] = WorkHistory.objects.all()

        return context


class OrgChartView(ListView):
    model = BasicProfile
    template_name = 'workforce/org_page.html'
    context_object_name = 'org_page'


class LoanDetailView(DetailView):
    model = Loans
    template_name = 'workforce/loan_detail_page.html'
    context_object_name = 'loan_detail'

    def get_context_data(self, **kwargs):
        context = super(LoanDetailView,self).get_context_data(**kwargs)
        context['loan_stat'] = Loans.objects.filter(pk=self.object.pk)\
                                    .annotate(payed=Sum('loan_payment__amount'))\
                                    .annotate(balance=F('amount')-F('payed'))\
                                    .order_by('trans_date')
        context['payments'] = Payment.objects.filter(base_loan=self.object).order_by('trans_date')

        return context


class FaceView(ListView):
    model = BasicProfile
    template_name = 'workforce/face_page.html'
    context_object_name = 'face_list'

    def get_context_data(self, **kwargs):
        context = super(FaceView,self).get_context_data(**kwargs)

        context['active'] = BasicProfile.objects.filter(employee_profile__employment_status='Active').order_by('lname')
        context['resigned'] = BasicProfile.objects.filter(employee_profile__employment_status='Resigned').order_by('lname')

        return context


class LeaveView(ListView):
    model = Leave
    template_name = 'workforce/leave_page.html'
    context_object_name = 'leave_list'

    def get_context_data(self, **kwargs):
        context = super(LeaveView,self).get_context_data(**kwargs)

        all_leaves = Leave.objects.filter(date_to__year = current_date.year)

        context['all'] = all_leaves
        context['for_approval'] = all_leaves.filter(approval='For Approval').order_by('create_date')
        context['approved'] = all_leaves.filter(approval__startswith='Approved').order_by('-date_from')[:10]
        context['denied'] = all_leaves.filter(Q(approval='Denied') | Q(approval='Canceled')).order_by('-date_from')[:10]

        return context


class DocumentView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FileDocument
    template_name = 'workforce/file_page.html'
    context_object_name = 'document_index'

    def get_context_data(self, **kwargs):
        context = super(DocumentView,self).get_context_data(**kwargs)

        context['for_renewal'] = FileDocument.objects.filter(expiry_date__lte=date.today())


        return context


    def test_func(self):
        return self.request.user.groups.filter(name='Workforce').exists()


class SubconView(LoginRequiredMixin, ListView):
    model = Subcon
    template_name = 'workforce/subcon_list.html'
    context_object_name = 'subcon_list'

    def get_context_data(self, **kwargs):
        context = super(SubconView,self).get_context_data(**kwargs)

        context['subcon_list'] = Subcon.objects.all()

        return context


def LogSearch(request):
    today = date.today()

    logs = LogEntry.objects.filter(action_time__date__month=today.month)

    search_logs = LogFilter(request.GET, queryset=logs)

    return render(request, 'workforce/logs_list.html', {'logs': search_logs,})

# **************************************************************
# START dongilay
# **************************************************************
def get_branchadmin_of_user(user):
    branch_admin = ''

    if user.branch == 'Baguio':
        # Penelope Lawangen
        branch_admin = BasicProfile.objects.get(id=96)
        # branch_admin = User.objects.get(id=1).basicprofile
    elif user.branch == 'Bontoc':
        # Qhenny Fuyag
        branch_admin = BasicProfile.objects.get(id=215)
    elif user.branch == 'Tagaytay':
        # Penelope Lawangen
        branch_admin = BasicProfile.objects.get(id=96)
    return branch_admin

class NewLeaveApplicationView(LoginRequiredMixin, CreateView):
    model = Leave
    template_name = 'workforce/leave_form.html'
    form_class = LeaveForm

    def form_valid(self, form):
        self.form = form
        leave_obj = form.save(commit=False)
        leave_obj.approved_by_super = self.request.user.basicprofile.employee_profile.supervisor
        leave_obj.save()
        return super().form_valid(form)

    def send_html_mail(self):
        mailer = AIPLeaveMailer(self.object, self.request)
        mailer.send_to_super()

    def send_sms(self):
        message = LeaveSMS(self.object, self.request)
        message.send_to_super()

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)

        self.send_html_mail()
        self.send_sms()

        url = reverse_lazy('workforce:leave_list')
        return url

    def get_initial(self):
        return {
            'base_profile': self.request.user.basicprofile
        }

class UpdateLeaveApplicationView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = 'workforce/update_leave_form.html'
    form_class = LeaveForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)

        return reverse_lazy('workforce:leave_list')

class SuperApproveLeaveView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = 'workforce/super_approve_leave_form.html'
    form_class = SuperLeaveForm

    def get_context_data(self, **kwargs):
        context = super(SuperApproveLeaveView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.form = form
        leave_obj = form.save(commit=False)
        if leave_obj.approval_super != 'Denied':
            leave_obj.approved_by = get_branchadmin_of_user(user=self.object.base_profile.employee_profile)

        leave_obj.save()
        return super().form_valid(form)

    def send_html_mail(self):
        mailer = AIPLeaveMailer(self.object, self.request)

        if self.object.approval_super == 'Denied':
            mailer.send_to_requestor()
        else:
            mailer.send_to_admin()

    def send_sms(self):
        message = LeaveSMS(self.object, self.request)
        if self.object.approval_super == 'Denied':
            message.send_to_requestor()
        else:
            message.send_to_admin()

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)

        self.send_html_mail()
        self.send_sms()

        return reverse_lazy('workforce:leave_list')

    def get_initial(self):

        return {
            'date_approved_super': date.today
        }

class AdminApproveLeaveView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = 'workforce/admin_approve_leave_form.html'
    form_class = AdminLeaveForm

    def get_context_data(self, *args, **kwargs):
        context = super(AdminApproveLeaveView, self).get_context_data( *args, **kwargs)

        context['object_branch_admin'] = self.object.approved_by
        return context

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def send_html_mail(self):
        mailer = AIPLeaveMailer(self.object, self.request)
        mailer.send_to_admin()

    def send_sms(self):
        message = LeaveSMS(self.object, self.request)
        message.send_to_requestor()

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)

        self.send_html_mail()
        self.send_sms()

        return reverse_lazy('workforce:leave_list')

    def get_initial(self):

        return {
            'date_approved': date.today
        }

class NewOutsiderView(LoginRequiredMixin, CreateView):
    model = Outsider
    template_name = 'workforce/outsider_form.html'
    form_class = OutsiderForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('workforce:profile_list')
        return url

class UpdateOutsiderView(LoginRequiredMixin, UpdateView):
    model = Outsider
    template_name = 'workforce/outsider_form.html'
    form_class = OutsiderForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('workforce:profile_list')

class NewSubconView(LoginRequiredMixin, CreateView):
    model = Subcon
    template_name = 'workforce/subcon_form.html'
    form_class = SubconForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('workforce:subcon_list')
        return url

class UpdateSubconView(LoginRequiredMixin, UpdateView):
    model = Subcon
    template_name = 'workforce/subcon_form.html'
    form_class = SubconForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('workforce:subcon_list')

class NewFileDocumentView(LoginRequiredMixin, CreateView):
    model = FileDocument
    template_name = 'workforce/filedocument_form.html'
    form_class = FileDocumentForm

    def get_success_url(self):
        add_log(self.request.user, self.model, self.object)
        url = reverse_lazy('workforce:file_index')
        return url

class UpdateFileDocumentView(LoginRequiredMixin, UpdateView):
    model = FileDocument
    template_name = 'workforce/filedocument_form.html'
    form_class = FileDocumentForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        change_log(user=self.request.user, modelIns=self.model, obj=self.object, form=self.form)
        return reverse_lazy('workforce:file_index')

# **************************************************************
# END dongilay
# **************************************************************
















