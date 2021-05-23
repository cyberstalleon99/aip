from django.conf.urls import url
from django.urls import path, re_path
from accounting import views

app_name = 'accounting'

urlpatterns = [
    #autocomplete
    path('purchase/by', views.FieldAutoComplete.as_view(), name='matic'),
    path('purchase/cash', views.CashAutoComplete.as_view(), name='cash'),
    path('purchase/request', views.PurchaseAutoComplete.as_view(), name='purchase'),
    path('purchase/site', views.SiteAutoComplete.as_view(), name='project_site'),
    path('purchase/item', views.ItemAutoComplete.as_view(), name='item_name'),
    path('purchase/supplier', views.SupplierAutoComplete.as_view(), name='supplier'),
    path('purchase/subcon', views.SubconAutoComplete.as_view(), name='subcon'),
    path('purchase/code', views.CodeAutoComplete.as_view(), name='code'),
    path('purchase/entry', views.EntryAutoComplete.as_view(), name='entry'),

    #accounting pages
    path('detail/entry/<pk>/', views.DetailEntryView.as_view(), name='detail_entry'),
    path('detail/entry/print/<pk>/', views.DetailEntryPrintView.as_view(), name='detail_entry_print'),
    path('your/entry/', views.YourEntryView.as_view(), name='your_entry'),
    path('cashiers/daily/', views.CashiersDailyView.as_view(), name='cashiers_daily'),
    path('for/verification/', views.ForVerificationView.as_view(), name='for_verification'),
    path('journal/entry/', views.SearchJournalEntry, name='journal_entry'),

    path('entry/status/<pk>/',views.entry_liquidated, name='update_entry_liquidated'),

    #entry crud
    path('new/entry/', views.NewEntryView.as_view(), name='new_entry'),
    path('new/entry/<pk>/', views.NewEntryView2.as_view(), name='new_entry2'),
    path('update/entry/<pk>/', views.UpdateEntryView.as_view(), name='update_entry'),
    path('delete/entry/<pk>/', views.DeleteEntryView.as_view(), name='delete_entry'),

    #fund request
    path('new/fund/request/', views.NewFundRequestView.as_view(), name='new_fr'),
    path('update/fund/request/<pk>/', views.UpdateFundRequestView.as_view(), name='update_fr'),
    path('delete/fund/request/<pk>/', views.DeleteFundRequestView.as_view(), name='delete_fr'),

    #subcon billing
    path('new/bill/request/', views.NewBillingView.as_view(), name='new_billing'),
    path('update/bill/request/<pk>/', views.UpdateBillingView.as_view(), name='update_billing'),
    path('delete/bill/request/<pk>/', views.DeleteBillingView.as_view(), name='delete_billing'),

    path('subcon/billing/',views.SubconBillingView.as_view(), name='billing_page'),
    path('ops/<pk>/',views.StatusOPS, name='status_ops'),
    path('acc/<pk>/',views.StatusACC, name='status_acc'),
    path('wh/<pk>/',views.StatusWH, name='status_wh'),

    #purchasing pages
    path('pending/',views.PendingView.as_view(), name='pending_page'),
    path('purchase/',views.PurchasedListView.as_view(), name='purchased_page'),
    path('purchased/entry/',views.PurchasedEntryView.as_view(), name='purchased_entry'),
    path('purchased/monitoring/',views.MonitoringView.as_view(), name='purchased_audit'),

    path('detail/por/<pk>/', views.DetailPORView.as_view(), name='detail_por'),
    path('purchase/detail/<pk>/', views.PurchaseDetailView.as_view(), name='purchase_detail_page'),

    path('utang/',views.CreditEntryView.as_view(), name='utang_page'),
    path('cancelled/',views.CancelledView.as_view(), name='cancelled_page'),
    path('item/',views.ItemView.as_view(), name='item_page'),
    path('listahan/',views.PriceListView.as_view(), name='price_list'),

    path('process/<pk>/',views.ProcessPOR, name='por_process'),
    path('cancel/<pk>/',views.CancelPOR, name='por_cancel'),
    path('invalid/<pk>/',views.InvalidPOR, name='por_invalid'),
    path('approve/<pk>/',views.ApprovePOR, name='por_approve'),
    path('today/<pk>/',views.TodayStatus, name='today_status'),

    #Purchase Order Request
    path('new/purchase/order/', views.NewPurchaseOrderView.as_view(), name='new_por'),
    path('update/purchase/order/<pk>/', views.UpdatePurchaseOrderView.as_view(), name='update_por'),
    path('delete/purchase/order/<pk>/', views.DeletePurchaseOrderView.as_view(), name='delete_por'),

    # **************************************************************
    # START dongilay
    # **************************************************************

    path('new/supplier/', views.NewSupplierView.as_view(), name='new_supplier'),
    path('update/supplier/<pk>/', views.UpdateSupplierView.as_view(), name='update_supplier'),

    path('new/item/', views.NewItemView.as_view(), name='new_item'),
    path('update/item/<pk>/', views.UpdateItemView.as_view(), name='update_item'),

    path('new/liquidation/', views.NewLiquidationView.as_view(), name='new_liquidation'),
    path('update/liquidation/<pk>/', views.UpdateLiquidationView.as_view(), name='update_liquidation'),

    # **************************************************************
    # END dongilay
    # **************************************************************

    #Old Links

    #accounting pages
    #path('',views.IndexView.as_view(), name='accounting_index'),    #For Liquidation
    #path('ca/detail/<pk>/', views.LiquidationDetailView.as_view(), name='ca_detail'), #For Luqidation - CA Detail
    #path('ca/print/<pk>/', views.LiquidationPrintView.as_view(), name='ca_print'),

    #new cash budget
    #path('cashbudget/new/', views.NewCashBudgetView.as_view(), name='new_cashbudget'),
    #path('cashbudget/update/<pk>/', views.UpdateCashBudgetView.as_view(), name='update_cashbudget'),

    #new liquidation
    #path('ca/liquidation/new/<pk>/', views.NewLiquidationView.as_view(), name='new_liquidation'),
    #path('ca/liquidation/update/<pk>/', views.UpdateLiquidationView.as_view(), name='update_liquidation'),
    #path('ca/liquidation/delete/<pk>/', views.DeleteLiquidationView.as_view(), name='delete_liquidation'),

    #path('bc/',views.BranchCashierView.as_view(), name='bc_page'),
    #path('bk/',views.BookKeeperView.as_view(), name='bk_page'),
    #path('books/',views.BooksView.as_view(), name='books_page'),
    #path('reports/',views.DailyReportView.as_view(), name='reports_page'),

    #re_path(r'^cash/(?P<pk>[-\w]+)/$', views.CashReceivedDetailView.as_view(), name='cash_received_page'),
    #re_path(r'^liquidation/(?P<pk>[-\w]+)/$', views.LiquidationDetailView.as_view(), name='liquidation_page'),
    #re_path(r'^cdv/(?P<pk>[-\w]+)/$', views.VoucherDetailView.as_view(), name='cdv_page'),



]
