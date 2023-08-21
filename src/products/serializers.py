from rest_framework import serializers

from .models import Product, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductsListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    tags = serializers.SerializerMethodField()  # Use SerializerMethodField

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category_name', 'price', 'created_at', 'tags']

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    