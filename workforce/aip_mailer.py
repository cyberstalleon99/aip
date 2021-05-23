from django.core.mail import send_mail
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from django.contrib import messages

class BaseAIPHtmlMail():
    _from = ''
    _subject = ''
    _recipient = []

    _ctx = {}
    _mail_template = ''

    email_status = ''
    EMAIL_STATUS = {
        'ERROR': 'ERROR',
        'SUCCESS': 'SUCCESS'
    }

    def __init__(self, sender, mail_template, subject='', recipient='', ctx=''):
        self._from = sender
        self._subject = subject
        self._recipient = recipient
        self._ctx = ctx
        self._mail_template = mail_template

    def get_recipients(self):
        return self._recipient

    def send(self):
        if self._recipient:
            try:
                message = get_template(self._mail_template).render(self._ctx)
                email_msg = EmailMessage (
                    self._subject,
                    message,
                    self._from,
                    self._recipient
                )
                email_msg.content_subtype = "html"
                email_msg.send()
            except:
                self.email_status = self.EMAIL_STATUS['ERROR']
            else:
                self.email_status = self.EMAIL_STATUS['SUCCESS']
        else:
            self.email_status = self.EMAIL_STATUS['ERROR']

        return self.email_status


class AIPLeaveMailer(BaseAIPHtmlMail):

    def __init__(self, leave_obj, request):
        super().__init__(sender='aip911dispatch@gmail.com', mail_template='workforce/mail.html')
        self._leave_obj = leave_obj
        self._request = request

        self.init_context()

    def do_send(self):
        email_status = self.send()
        if email_status == self.EMAIL_STATUS['SUCCESS']:
            recipients_str = ', '.join(self.get_recipients())
            messages.success(self._request, f"Email was SUCCESSFULLY sent to {recipients_str}!")
        else:
            messages.error(self._request, "Something went wrong! Your request was still saved. Please contact R&D")

    def init_context(self):
        self._ctx = {
            'intro_msg': "An application for leave is on que, and needs your attention!",
            'requested_by': self._leave_obj.base_profile.fullname(),
            'date_of_leave': f"{self._leave_obj.date_from.strftime('%d %b, %Y')} - {self._leave_obj.date_to.strftime('%d %b, %Y')}",
            'totals_days': str(self._leave_obj.total_days),
            'reason': self._leave_obj.reason,
        }

    def send_to_super(self):
        try:
            self._recipient = [self._leave_obj.approved_by_super.email]
        except:
            self._recipient = None

        self._subject = '[NEW]Leave Application: ' + str(self._leave_obj.base_profile)
        self._ctx['link'] = f"https://eakdev.pythonanywhere.com/workforce/approve/leave/{self._leave_obj.id}/super/"
        self.do_send()

    def send_to_admin(self):
        try:
            self._recipient = [self._leave_obj.approved_by.email]
        except:
            self._recipient = None

        self._subject = '[UPDATE]Leave Application: ' + str(self._leave_obj.base_profile)

        self._ctx['link'] = f"https://eakdev.pythonanywhere.com/workforce/approve/leave/{self._leave_obj.id}/admin/"
        self._ctx['status_super'] = f"{self._leave_obj.approval_super} by {self._leave_obj.approved_by_super.fullname()}"
        self._ctx['remarks_super'] = self._leave_obj.remarks_super
        self.do_send()

    def send_to_requestor(self):
        self._recipient = [self._leave_obj.base_profile.email]
        self._subject = '[UPDATE]Leave Application: ' + str(self._leave_obj.base_profile)

        self._ctx['link'] = f"https://eakdev.pythonanywhere.com/workforce/update/leave/{self._leave_obj.id}/"

        if self._leave_obj.approval_super != 'Denied':
            self._ctx['status_admin'] = f"{self._leave_obj.approval} by {self._leave_obj.approved_by.fullname()}"
            self._ctx['remarks_admin'] = self._leave_obj.remarks
        else:
            self._ctx['status_super'] = f"{self._leave_obj.approval_super} by {self._leave_obj.approved_by_super.fullname()}"
            self._ctx['remarks_super'] = self._leave_obj.remarks_super
        self.do_send()
