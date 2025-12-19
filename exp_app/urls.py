from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('',DashboardView.as_view(),name='dashboard'),
    path('transaction/add/',TransactionCreateView.as_view(),name='transaction'),
    path('goal/add/',GoalCreateView.as_view(),name='goal'),
    path('transactions/',TransactionListView.as_view(),name='transaction_list'),
    path('goal_list/',GoalListView.as_view(),name='goal_list'),
    path('transaction_report/',export_transaction,name='transaction_report'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('profile/delete/', profile_delete, name='profile_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)