from .views import *
from django.urls import path

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('',DashboardView.as_view(),name='dashboard'),
    path('transaction/add/',TransactionCreateView.as_view(),name='transaction'),
]