from django.urls import path
from product import views

urlpatterns = [
 path("", views.view_categoty, name = "categoty_list"),
 path("<int:pk>", views.view_specific_category, name = "view_specific_category"),
]