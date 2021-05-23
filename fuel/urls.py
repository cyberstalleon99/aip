from django.conf.urls import url
from django.urls import path, re_path
from fuel import views

app_name = 'fuel'

urlpatterns = [
    #path('',views.IndexView.as_view(), name='fuel_index'),
    path('dash',views.IndexView.as_view(), name='dash_index'),
    path('add_reading',views.ReadingCreateView.as_view(), name='new_reading'),
    path('update_reading/<int:pk>', views.ReadingUpdateView.as_view(), name='update_reading'),
    path('add_transaction',views.TransactionCreateView.as_view(), name='new_transaction'),
    path('update_transaction/<int:pk>', views.TransactionUpdateView.as_view(), name='update_transaction'),
    path('add_tank',views.TankCreateView.as_view(), name='new_tank'),
    path('update_tank/<int:pk>', views.TankUpdateView.as_view(), name='update_tank'),

    # **************************************************************
    # START dongilay
    # **************************************************************

    path('tanks/', views.TankAutoComplete.as_view(), name='tanks'),

    path('new/transaction/', views.NewTransactionView.as_view(), name='new_transaction'),
    path('update/transaction/<pk>/', views.UpdateTransactionView.as_view(), name='update_transaction'),

    path('new/reading/', views.NewReadingView.as_view(), name='new_reading2'),
    path('update/reading/<pk>/', views.UpdateReadingView.as_view(), name='update_reading2'),

    path('new/tank/', views.NewTankView.as_view(), name='new_tank2'),
    path('update/tank/<pk>/', views.UpdateTankView.as_view(), name='update_tank2'),

    # **************************************************************
    # END dongilay
    # **************************************************************

]
