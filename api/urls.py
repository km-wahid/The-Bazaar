from django.urls import path, include
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet, ProductImageViewSet
from orders.views import CartViewSet, CartItemViewSet, OrderViewset
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewset, basename='orders')

product_router = NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-reviews')
product_router.register('images', ProductImageViewSet,
                        basename='product-images')


cart_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
