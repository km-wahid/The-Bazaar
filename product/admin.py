from django.contrib import admin
from product.models import Review, Product, Category
# Register your models here.
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Category)