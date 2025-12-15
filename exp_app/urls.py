from .views import *
from django.urls import path

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('',DashboardView.as_view(),name='dashboard'),
    path('transaction/add/',TransactionCreateView.as_view(),name='transaction'),
    path('goal/add/',GoalCreateView.as_view(),name='goal'),
    path('transactions/',TransactionListView.as_view(),name='transaction_list'),
    path('goal_list/',GoalListView.as_view(),name='goal_list'),
    path('transaction_report/',export_transaction,name='transaction_report'),
    # path('search_transactions/',search_transactions,name='search_transactions'),
]