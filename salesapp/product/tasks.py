# product/tasks.py
from celery import shared_task
from PIL import Image
from .models import Product
import os

@shared_task
def process_product_image(product_id):
    product = Product.objects.get(id=product_id)
    if product.image:
        img = Image.open(product.image.path)
        img = img.resize((300, 300))  # Example resize
        img.save(product.image.path)