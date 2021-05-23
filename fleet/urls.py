from django.conf.urls import url
from django.urls import path, re_path
from fleet import views

app_name = 'fleet'

urlpatterns = [
    #autocomplete
    path('units/', views.UnitAutoComplete.as_view(), name='units'),

    path('dash/',views.DashView.as_view(), name='dash_page'),
    path('padala/',views.DeliveryView.as_view(), name='delivery_page'),
    path('padala/mirror/',views.DeliveryMirrorView.as_view(), name='delivery_mirror'),
    path('travel/',views.TravelView.as_view(), name='travel_page'),
    path('travel/status/<pk>/',views.TravelStatus, name='change_status'),
    path('calendar/',views.CalendarView.as_view(), name='calendar_page'),
    path('wo/',views.WorkOrderView.as_view(), name='wo_page'),
    path('all/wo/',views.WorkOrderSearchView.as_view(), name='all_wo'),


    path('gallery/',views.GalleryView.as_view(), name='fleet_gallery'),
    re_path(r'^detail/(?P<pk>[-\w]+)/$', views.UnitDetailView.as_view(), name='unit_detail'),

    re_path(r'^jo/detail/(?P<pk>[-\w]+)/$', views.JoDetailView.as_view(), name='jo_detail'),

    path('map/',views.UnitMapView.as_view(), name='fleet_map'),
    path('stats/',views.StatView.as_view(), name='fleet_stat'),

    path('ur/', views.UtilizationReportView.as_view(), name='ur_page'),
    path('upload-ur/', views.ur_upload, name="ur_upload"),

    # **************************************************************
    # START dongilay
    # **************************************************************

    path('new/travel/', views.NewTravelView.as_view(), name='new_travel'),
    path('update/travel/<pk>/', views.UpdateTravelView.as_view(), name='update_travel'),

    path('all/travel/', views.TravelSearchView.as_view(), name='all_travel'),

    # **************************************************************
    # END dongilay
    # **************************************************************
]
