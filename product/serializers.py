from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product, Review, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'description', 'product_count']
        
    # product_count = serializers.SerializerMethodField(method_name="product_count")
    product_count = serializers.IntegerField(read_only= True)
        
    # def get_product_count(self, category):
    #     count = Product.objects.filter(category=category).count()
    #     return count
    
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source= 'price')
#     # category = serializers.PrimaryKeyRelatedField(queryset= Category.objects.all())
#     # category = serializers.StringRelatedField()
#     # category = CategorySerializer()
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name = 'view_specific_category',
#     )
    
#     price_with_tax = serializers.SerializerMethodField(
#         method_name= "calculate_tax")
        
#     def calculate_tax(self, product):
#         return round(product.price * Decimal(1.1), 2)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock','images', 'category', 'created_at', 'updated_at']
        
        
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'view_specific_category',
    # )
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price Could not be negative")
        return price
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user','product','ratings', 'comment']
        read_only_fields = ['user', 'product']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
        
        
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']