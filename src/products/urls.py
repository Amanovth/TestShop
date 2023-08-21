from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductsListAPIView.as_view(), name='products-list'),
    path('export/', ProductsExportExcelAPIView.as_view(), name='export-to-exel')
]