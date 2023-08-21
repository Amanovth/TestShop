from openpyxl import Workbook
from rest_framework import views, permissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.cache import cache

from .models import Product
from .serializers import ProductsListSerializer


class ProductsListAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        cached_data = cache.get('product_list')
        
        
        if cached_data is not None:
            print('================== data from cache ==================')
            return Response(cached_data)
        
        queryset = Product.objects.select_related('category').prefetch_related('tags')
        serializer = ProductsListSerializer(queryset, many=True)
        
        cache.set('product_list', serializer.data, timeout=3600)
        
        return Response(serializer.data)


class ProductsExportExcelAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        products = Product.objects.select_related('category').prefetch_related('tags')
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Products'
        
        column_widths = {
            'B': 30,  # Name
            'C': 40,  # Description
            'D': 20,  # Category
            'E': 15,  # Price
            'F': 20,  # Created At
            'G': 50   # Tags
        }

        for column, width in column_widths.items():
            sheet.column_dimensions[column].width = width
        
        sheet.append(['ID', 'Name', 'Description', 'Category', 'Price', 'Created At', 'Tags'])
        
        for product in products:
            sheet.append([
                product.id,
                product.name,
                product.description,
                product.category.name,
                product.price,
                product.created_at.replace(tzinfo=None),
                ', '.join([tag.name for tag in product.tags.all()])
            ])
            
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        workbook.save(response)
        
        return response