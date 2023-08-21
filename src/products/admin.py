from django.contrib import admin
from .models import Product, Category, Tag


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'created_at',)
    list_display_links = ('id', 'name')
    

admin.site.register(Tag)
admin.site.register(Category)