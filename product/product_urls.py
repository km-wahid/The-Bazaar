
from django.urls import path
from product import views

urlpatterns = [
 path("<int:pk>/", views.view_specific_products, name = "specfic_products"),   
 path("", views.view_product, name = "products-list"),   
]