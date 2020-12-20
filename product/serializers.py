
from rest_framework import serializers
from .models import Product, ProductDetail


class ProductDetailSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ProductDetail
		fields = '__all__'

		
class ProductSerializer(serializers.ModelSerializer):
	#variations = serializers.PrimaryKeyRelatedField(many = True,queryset = ProductDetail.objects.all())
	variations = ProductDetailSerializer(many = True)
	class Meta:
		model = Product
		fields = ['id','variations','category','name','description','price']


