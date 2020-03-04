from django.urls import path
from .views import *

urlpatterns = [
    path('', all_currencies, name='currencies'),
    path('currency_history/<int:id>', currency_history, name='currency_history'),
    path('currency_history/<int:id>/by_period/', currency_history_by_period, name='currency_history_by_period'),
    path('currency_history/delete/<int:pk>/', CurrencyHistoryDeleteView.as_view(), name='delete_currency_history'),
    path('currency_history/<int:id>/add/', CurrencyHistoryCreateView.as_view(), name='add_currency_history'),
]
