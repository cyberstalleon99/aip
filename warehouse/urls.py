from django.urls import path, re_path
from warehouse import views

app_name = 'warehouse'

urlpatterns = [
    path('dash/',views.DashView.as_view(), name='dash_page'),
    path('stats/',views.StatsView.as_view(), name='stats_page'),

    path('sinumrek/', views.IncomingSearch, name='sinumrek'),
    path('linumwar/', views.OutgoingSearch, name='linumwar'),

    path('sinumrek/status/<pk>/',views.IncomingStatus, name='in_status'),
    path('linumwar/status/<pk>/',views.OutgoingStatus, name='out_status'),

    path('verification/',views.AnalystPageView.as_view(), name='verification'),

    re_path(r'^detail/main/(?P<pk>[-\w]+)/$', views.DetailViewMain.as_view(), name='detail_main'),
    re_path(r'^detail/project/(?P<pk>[-\w]+)/$', views.DetailView.as_view(), name='detail_project'),
    re_path(r'^purchase/(?P<pk>[-\w]+)/$', views.DailyPurchaseView.as_view(), name='daily_purchase_page'),

    re_path(r'^item/detail/(?P<pk>[-\w]+)/$', views.CheckerDetailView.as_view(), name='checker_page'),

    re_path(r'^fuel/(?P<pk>[-\w]+)/$', views.FuelView.as_view(), name='fuel_page'),

    # **************************************************************
    # START dongilay
    # **************************************************************

    #incoming
    path('new/incoming/', views.NewIncomingView.as_view(), name='new_incoming'),
    path('new/incoming/<pk>/', views.NewIncomingView.as_view(), name='new_incoming_site'),
    path('update/incoming/<pk>/', views.UpdateIncomingView.as_view(), name='update_incoming'),
    path('detail/incoming/<pk>/', views.DetailIncomingView.as_view(), name='detail_incoming'),

    #outgoing
    path('new/outgoing/base_in/<pk>/', views.NewOutgoingView.as_view(), name='new_outgoing'),
    path('update/outgoing/<pk>/base_in/<incoming_id>/', views.UpdateOutgoingView.as_view(), name='update_outgoing'),

    # **************************************************************
    # END dongilay
    # **************************************************************

]