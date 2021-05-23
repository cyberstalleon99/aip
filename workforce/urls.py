from django.urls import path, re_path
from workforce import views

app_name = 'workforce'

urlpatterns = [
    #autocomplete
    path('workforce/outsiders', views.OutsiderAutoComplete.as_view(), name='outsiders'),

    path('',views.IndexView.as_view(), name='profile_list'),
    path('subcon/',views.SubconView.as_view(), name='subcon_list'),
    re_path(r'^detail/(?P<pk>[-\w]+)/$', views.ProfileDetailView.as_view(), name='profile_detail'),
    re_path(r'^loan/(?P<pk>[-\w]+)/$', views.LoanDetailView.as_view(), name='loan_detail_page'),

    path('leaves/',views.LeaveView.as_view(), name='leave_list'),
    path('file/',views.DocumentView.as_view(), name='file_index'),
    path('faces/',views.FaceView.as_view(), name='face_list'),

    path('notifications/',views.NotificationsView.as_view(), name='notif_page'),
    path('hidden/',views.BenefitsView.as_view(), name='benefit_page'),
    path('chart/',views.OrgChartView.as_view(), name='org_page'),

    path('logs/',views.LogSearch, name='logs_list'),

    # **************************************************************
    # START dongilay
    # **************************************************************

    path('new/leave/', views.NewLeaveApplicationView.as_view(), name='new_leave'),
    path('update/leave/<pk>/', views.UpdateLeaveApplicationView.as_view(), name='update_leave'),
    path('approve/leave/<pk>/super/', views.SuperApproveLeaveView.as_view(), name='approve_leave_super'),
    path('approve/leave/<pk>/admin/', views.AdminApproveLeaveView.as_view(), name='approve_leave_admin'),

    path('new/outsider/', views.NewOutsiderView.as_view(), name='new_outsider'),
    path('update/outsider/<pk>/', views.UpdateOutsiderView.as_view(), name='update_outsider'),

    path('new/subcon/', views.NewSubconView.as_view(), name='new_subcon'),
    path('update/subcon/<pk>/', views.UpdateSubconView.as_view(), name='update_subcon'),

    path('new/filedocument/', views.NewFileDocumentView.as_view(), name='new_filedocument'),
    path('update/filedocument/<pk>/', views.UpdateFileDocumentView.as_view(), name='update_filedocument'),

    # Autocomplete URLs
    path('basic_profiles/', views.BasicProfileAutoComplete.as_view(), name='basic_profiles'),

    # **************************************************************
    # END dongilay
    # **************************************************************

]
