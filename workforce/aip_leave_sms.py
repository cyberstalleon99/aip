from fleet.aip_sms_sender import BaseAIPSms
from django.contrib import messages

class LeaveSMS(BaseAIPSms):

    def __init__(self, leave_obj, request):
        self._leave_obj = leave_obj
        self._request = request
        self.client_init()

    def do_send(self):
        sms_status = self.send()
        if sms_status == self.SMS_STATUS['SUCCESS']:
            recipients_str = ', '.join(self.get_recipients())
            messages.success(self._request, f"SMS was SUCCESSFULLY sent to {recipients_str}!")
        else:
            messages.error(self._request, "Something went wrong! Your request was still saved. Please check the ff: Twilio Load Balance, Verified/Correct Phone Number or contact R&D!")

    def send_to_super(self):

        # supervisor = [self._leave_obj.base_profile.employee_profile.supervisor.mobile]
        try:
            supervisor = [self._leave_obj.base_profile.employee_profile.supervisor.mobile]
        except:
            supervisor = None

        intro_msg = "Leave Application"
        requested_by = f"Requested by: {self._leave_obj.base_profile.fullname()}"
        date_of_leave = f"Date: {self._leave_obj.date_from} - {self._leave_obj.date_to}"
        reason = f"Reason: {self._leave_obj.reason[:10]}..."
        link = f"See more: https://eakdev.pythonanywhere.com/workforce/approve/leave/{self._leave_obj.id}/super/"

        sms_content = f"\n{intro_msg} \
                        \n{requested_by} \
                        \n{date_of_leave} \
                        \n{reason} \
                        \n{link}"

        self.set_msg_body(sms_content)
        self.set_recipients(supervisor)
        self.do_send()

    def send_to_admin(self):
        # admin = [self._leave_obj.approved_by.mobile]
        try:
            admin = [self._leave_obj.approved_by.mobile]
        except:
            self._recipient = None

        intro_msg = "Leave Application"
        requested_by = f"Requested by: {self._leave_obj.base_profile.fullname()}"
        date_of_leave = f"Date: {self._leave_obj.date_from} - {self._leave_obj.date_to}"
        reason = f"Reason: {self._leave_obj.reason[:10]}..."
        status = f"Status: {self._leave_obj.approval_super} by {self._leave_obj.approved_by_super.fullname()}"
        link = f"See more: https://eakdev.pythonanywhere.com/workforce/approve/leave/{self._leave_obj.id}/admin/"

        sms_content = f"\n{intro_msg} \
                        \n{requested_by} \
                        \n{date_of_leave} \
                        \n{reason} \
                        \n{status} \
                        \n{link}"

        self.set_msg_body(sms_content)
        self.set_recipients(admin)
        self.do_send()

    def send_to_requestor(self):
        requestor = [self._leave_obj.base_profile.mobile]
        intro_msg = "Leave Application"
        requested_by = f"Requested by: {self._leave_obj.base_profile.fullname()}"
        date_of_leave = f"Date: {self._leave_obj.date_from} - {self._leave_obj.date_to}"
        # reason = f"Reason: {self._leave_obj.reason[:10]}..."
        status = f"Approval by Supervisor: {self._leave_obj.approval_super} by {self._leave_obj.approved_by_super.fullname()}"
        if self._leave_obj.approval_super == 'Denied':
            status_admin = ""
        else:
            status_admin = f"Approval by Admin: {self._leave_obj.approval} by {self._leave_obj.approved_by_super.fullname()}"

        sms_content = f"\n{intro_msg} \
                        \n{requested_by} \
                        \n{date_of_leave} \
                        \n{status} \
                        \n{status_admin}"

        self.set_msg_body(sms_content)
        self.set_recipients(requestor)
        self.do_send()

