from rest_framework.views import APIView
from fleet.models import Travel
from rest_framework.response import Response
from workforce.constants import (STATUS_TRAVEL)
from django.utils import timezone
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

TRANS_STATUS = {
    'SUCCESS': ['\033[92m', 'SUCCESS'],
    'FAILED': ['\033[91m', 'FAILED'],
    'INFO': ['\033[93m', 'NOTHING RECORDED']
}

def set_status(travel_entry, next_status):
    travel_entry.status = next_status
    curr_dttm = timezone.now()
    response = {
        'trans_status': TRANS_STATUS['SUCCESS'],
        'curr_status': next_status
    }

    if next_status == 'On its way':
        response['message'] = "Apan kan ngarud. DRIVE SAFE Apo!"
        response['dttm_logged'] = curr_dttm
        travel_entry.started_at = curr_dttm
    elif next_status == 'Arrived':
        response['message'] = "Inmay ka gayam Apo. Ustu man."
        response['dttm_logged'] = curr_dttm
        travel_entry.arrived_at = curr_dttm
    elif next_status == 'Coming back':
        response['message'] = "Agsubli kan ngarud. DRIVE SAFE Apo!"
        response['dttm_logged'] = curr_dttm
        travel_entry.returning_at = curr_dttm
    elif next_status == 'Returned':
        response['message'] = "Sinmubli kan gayam. Mayat man."
        response['dttm_logged'] = curr_dttm
        travel_entry.returned_at = curr_dttm

    travel_entry.save()

    return response

def on_its_way(travel_entry):
    return set_status(travel_entry, 'On its way')

def arrived(travel_entry):
    return set_status(travel_entry, 'Arrived')

def returning(travel_entry):
    return set_status(travel_entry, 'Coming back')

def returned(travel_entry):
    return set_status(travel_entry, 'Returned')


class TravelView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_curr_travel(self, body_num):
        curr_travel = ''
        try:
            curr_travel = Travel.objects.filter(base_unit__body_no=body_num).exclude(status='Scheduled').exclude(status='Returned').exclude(status='Canceled')
            curr_travel = curr_travel.order_by('date_start').first()
        except:
            curr_travel = ''
        else:
            curr_travel = curr_travel
        return curr_travel

    def patch(self, request):
        response = ''
        trans_type = request.data.pop('transaction_type')
        body_num_from_req = request.data.pop('body_num').strip()

        response = {
            # 'travel_entry': travel_entry.status,
            'trans_type': trans_type,
            'body_number': body_num_from_req
        }

        curr_travel = self.get_curr_travel(body_num_from_req)

        if curr_travel:
            response['prev_status'] = curr_travel.status
            if trans_type == "Out":
                if curr_travel.status == 'Travel Booked':
                    response['msg'] = on_its_way(curr_travel)
                elif curr_travel.status == 'Arrived':
                    response['msg'] = returning(curr_travel)
                elif curr_travel.status == 'On its way' or curr_travel.status == 'Coming back':
                    response['msg'] = {
                        'trans_status': TRANS_STATUS['FAILED'],
                        'message': "Adda pay naka %s nga travel mu. Pakicheck iti dispatch. Salamat Apo." %(curr_travel.status)
                    }

            elif trans_type == "In":
                if curr_travel.status == 'On its way':
                    response['msg'] = arrived(curr_travel)
                elif curr_travel.status == 'Coming back':
                    response['msg'] = returned(curr_travel)
                elif curr_travel.status == 'Arrived':
                    response['msg'] = {
                        'trans_status': TRANS_STATUS['FAILED'],
                        'message': "Nalipatam nga nag-OUT idjay nagapwam. Pakicheck iti dispatch. Salamat Apo."
                    }
                else:
                    response['msg'] = {
                        'trans_status': TRANS_STATUS['FAILED'],
                        'message': "Adda ti nakschedule nga travel na dytuy %s ngem haan pay naka-OUT. Pakicheck iti dispatch. Salamat Apo." %(body_num_from_req)
                    }

        else:
            response['msg'] = {
                'trans_status': TRANS_STATUS['FAILED'],
                'message': "Awan ti nakschedule nga travel na dytuy %s. Pakicheck iti dispatch. Salamat Apo." %(body_num_from_req)
            }

        return Response(response)


    def get(self, request):

        return Response({
            'test': "This is a test response"
        })

class SMSStatusCallbackView(APIView):

    def post(self, request, format=None):
        print(request.POST)
        f= open("smscallback.txt", "a")
        f.write(request.POST.get('MessageStatus'))
        f.close()
        test = {
            'test': 'asdfasdf'
        }
        return Response(test)
