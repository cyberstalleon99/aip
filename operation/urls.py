from django.urls import path, re_path
from operation import views

app_name = 'operation'

urlpatterns = [
    path('',views.IndexView.as_view(), name='project_index'),
    path('stats',views.StatsView.as_view(), name='stat_page'),
    re_path(r'^detail/(?P<pk>[-\w]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),

]
