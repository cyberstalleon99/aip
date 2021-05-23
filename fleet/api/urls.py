from django.urls import path
from .views import TravelView, SMSStatusCallbackView

app_name = "api_fleet"
urlpatterns = [
    path("travel/", TravelView.as_view(), name="travel-list"),
    path("travel/update/", TravelView.as_view(), name="travel-update"),

    path("sms_callback/", SMSStatusCallbackView.as_view(), name="sms-callback"),
]