from django.urls import path
from . import views

app_name = "tutorials"

urlpatterns = [
    path('', views.LatestTutorailsView.as_view(), name='latest1'),
    path('latest/', views.LatestTutorailsView.as_view(), name='latest'),

    path('new/tutorial/', views.NewTutorialView.as_view(), name='new_tutorial'),
    path('update/tutorial/<slug:slug>/', views.UpdateTutorialView.as_view(), name='update_tutorial'),
    path('detail/tutorial/<pk>/<str:q>/', views.DetailTutorialView.as_view(), name='detail_tutorial'),

    path('tag/<slug:tag_slug>/tutorial/<slug:tut_slug>/', views.tagged, name='tagged'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('department/<pk>/', views.DepartmentTutorialsView.as_view(), name='department_tutorials'),
]