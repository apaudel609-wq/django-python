from django.urls import path
from .views import add_transaction, TransactionListView

urlpatterns = [
    path('add/', add_transaction, name='add_transaction'),
    path('list/', TransactionListView.as_view(), name='transaction_list'),
    path('', TransactionListView.as_view(), name='transaction_index'),
]
