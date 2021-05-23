# **************************************************************
# START dongilay
# **************************************************************
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages


class BaseAIPSms():

    SMS_STATUS = {
        'ERROR': 'ERROR',
        'SUCCESS': 'SUCCESS'
    }

    twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_num = settings.TWILIO_NUMBER
    client = ''

    msg_body = ''
    recipients = []

    sms_status = ''

    def client_init(self):
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def get_num_str(self, num):
        return f"+63{str(num)[-10:]}"

    def set_recipients(self, recipients):
        try:
            recipients_str = map(self.get_num_str, recipients)
            self.recipients = list(recipients_str)
        except:
            self.recipients = None

    # def __init__(self, msg_body, recipients=None):
    def __init__(self, msg_body, recipients):
        self.msg_body = msg_body
        self.recipients = self.set_recipients(recipients)
        self.client_init()

    def get_recipients(self):
        return self.recipients

    def set_msg_body(self, msg_body):
        self.msg_body = msg_body

    def send(self):
        if self.recipients:
            for recipient in self.recipients:
                try:
                    # recipient_str = str(recipient)[-10:]
                    message = self.client.messages.create(\
                        body = self.msg_body,
                        from_ = self.twilio_num,
                        to = recipient
                    )
                except:
                    self.sms_status = self.SMS_STATUS['ERROR']
                else:
                    self.sms_status = self.SMS_STATUS['SUCCESS']
        else:
            self.sms_status = self.SMS_STATUS['ERROR']

        return self.sms_status

# ********************************************************************

class TravelSms(BaseAIPSms):

    # Number Sir Craig
    dispatch_num = '+639097584001'
    # dispatch_num = '+639463233452'

    travel_obj = ''
    recipients = []

    def __init__(self, travel_obj):
        self.travel_obj = travel_obj
        super().client_init()

    def do_send(self):
        sms_status = super().send()
        if sms_status == super().SMS_STATUS['SUCCESS']:
            recipients_str = ', '.join(super().get_recipients())
            messages.success(self.travel_obj.request, f"SMS was SUCCESSFULLY sent to {recipients_str}!")
        else:
            messages.error(self.travel_obj.request, "Something went wrong! Please check the ff: Twilio Load Balance, Verified/Correct Phone Number(Requestor, Driver)!")

    def send_new(self):
        request_by = f"Request by: {self.travel_obj.object.requested_by.fullname()}"
        travel_date = f"Travel Date: {self.travel_obj.object.date_start}"
        route = f"Route: {self.travel_obj.object.get_route()}"
        trip = f"Trip: {self.travel_obj.object.trip}"
        details = f"Details: {self.travel_obj.object.note[:10]}..."
        link = f"https://eakdev.pythonanywhere.com/fleet/update/travel/{self.travel_obj.object.id}/"
        sms_content = f"\n{request_by}\n{travel_date}\n{route}\n{trip}\n{details}\n{link}"

        super().set_msg_body(sms_content)
        super().set_recipients([self.dispatch_num])

        self.do_send()

    def send_update(self):
        request_by = f"Request by: {self.travel_obj.object.requested_by.fullname()}"
        travel_date = f"Travel Date: {self.travel_obj.object.date_start}"
        route = f"Route: {self.travel_obj.object.get_route()}"
        trip = f"Trip: {self.travel_obj.object.trip}"
        details = f"Details: {self.travel_obj.object.note[:10]}..."
        unit = f"Unit: {self.travel_obj.object}"
        driver = f"Driver: {self.travel_obj.object.driver}"
        status = f"Status: {self.travel_obj.object.status}"
        sms_content = f"\n{request_by}\n{travel_date}\n{route}\n{trip}\n{driver}\n{unit}\n{status}\n{details}"

        super().set_msg_body(sms_content)

        recip_nums = [self.travel_obj.object.requested_by.mobile, self.travel_obj.object.driver.mobile]
        super().set_recipients(recip_nums)
        self.do_send()



# **************************************************************
# END dongilay
# **************************************************************