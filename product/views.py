from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category
from product.serializers import ProductSerializer,CategorySerializer
from django.db.models import Count
from rest_framework import status
# Create your views here.
@api_view(['GET','POST'])
def view_product(request):
    if request.method == "GET":
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method =="POST":
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED, context={'request': request})
    else:
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET','PUT','DELETE'])
def view_specific_products(request,pk):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk =pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    if request.method == "PUT":
        product = get_object_or_404(Product, pk =pk)
        serializer = ProductSerializer(product,data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == "DELETE":
        product = get_object_or_404(Product, pk = pk)
        copy_of_product = product
        product.delete()
        serializer = ProductSerializer(copy_of_product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        
        
        
    
    
@api_view()
def view_categoty(request):
   category = Category.objects.annotate(product_count = Count('products')).all()
   serializer = CategorySerializer(category, many=True)
   return Response(serializer.data)
    
@api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)