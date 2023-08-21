from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from django.core.cache import cache


@receiver(post_save, sender=Product)
def invalidate_product_list_cache(sender, instance, **kwargs):
    print('================== cache invalidated ==================')
    cache.delete('product_list')