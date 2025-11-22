from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TransactionViewSet
from .views import (
    add_transaction, 
    TransactionListView, 
    TransactionDetailView, 
    TransactionUpdateView, 
    TransactionDeleteView,
    CategoryCreateView, 
    CategoryListView,
    DashboardView
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='api-transaction')

urlpatterns = [
    path('add/', add_transaction, name='add_transaction'),
    path('list/', TransactionListView.as_view(), name='transaction_list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('categories/add/', CategoryCreateView.as_view(), name='add_category'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('', TransactionListView.as_view(), name='transaction_index'),
    path('api/', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
