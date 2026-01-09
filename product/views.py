from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category, Review
from product.serializers import ProductSerializer,CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filter import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DeafultPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import DjangoModelPermissions
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category_id', 'price']
    filterset_class = ProductFilter
    pagination_class = DeafultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'id']
    permission_classes = [DjangoModelPermissions]
    
    # def get_permission(self):
    #     if self.request.method =='GET':
    #         return [AllowAny()]
    #     if self.request.method == 'POST':
    #         return [IsAdminUser()]
        
    
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get('category_id')
        
    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id=category_id)
    #         return queryset
    
    
    def distroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response ({'message': "You can't delete product when stock is more that 10"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class CategoryViewSet(ModelViewSet):
     queryset = Category.objects.annotate(
         product_count=Count('products')).all()
     
     serializer_class = CategorySerializer
     
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'] )
    
    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
        
    
# class ViewProduct(APIView):
#     def get(self, request):
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status= status.HTTP_201_CREATED, context={'request': request})

# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.select_related('category').all()
#     def get_serializer_class(self):
#         return ProductSerializer
#     def get_serializer_context(self):
#         return {'request': self.request}

    
# class ViewSpecificProduct(APIView):
#     def get(self, request, pk): 
#         product = get_object_or_404(Product, pk =pk)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#     def put(self, request, pk): 
#         product = get_object_or_404(Product, pk =pk)
#         serializer = ProductSerializer(product,data = request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#     def delete(self, request, pk): 
#         product = get_object_or_404(Product, pk = pk)
#         copy_of_product = product
#         product.delete()
#         serializer = ProductSerializer(copy_of_product, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
          
        
        
    


# class ViewCategory(APIView):
#     def get(self, request):
#         category = Category.objects.annotate(product_count = Count('products')).all()
#         serializer = CategorySerializer(category, many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = CategorySerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED) 
    
# class CategoryList(ListCreateAPIView):
#     def get_queryset(self):
#         return  Category.objects.annotate(product_count = Count('products')).all()
#     def get_serializer_class(self):
#         return CategorySerializer


# class ViewSpecifCategory(APIView):
#     def get(self, request, pk):
#         # category = get_object_or_404(Category, pk=pk)
#         category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)

#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
#         serializer = CategorySerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         category =get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
#         category.delete()
#         return Response(status=status.HTTP_400_BAD_REQUEST)
