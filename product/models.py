from django.db import models
from django.contrib.auth.models import User 
from users.models import Address
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name 


class Product(models.Model):
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	description = models.TextField()
	price = models.IntegerField()
	discount_price = models.IntegerField(default=0)

	def __str__(self):
		return self.name + ' ' + '(' + self.category.name + ')'	


class ProductDetail(models.Model):
	sizes = [
	('S','small'),
	('M','medium'),
	('L','large'),
	('XL','x-large')
	]
	colors = [
	('Blue','Blue'),
	('Black','Black'),
	('White','White'),
	('Orange','Orange'),
	('Green','Green'),
	('Yellow', 'Yellow'),
	('Grey', 'Grey'),
	('Red', 'Red')
	]
	product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variations")
	image1 = models.ImageField(default="default-product.jpg",upload_to="products")
	image2 = models.ImageField(default="default-product.jpg",upload_to="products")
	image3 = models.ImageField(default="default-product.jpg",upload_to="products")
	image4 = models.ImageField(default="default-product.jpg",upload_to="products")
	size = models.CharField(max_length=2,choices=sizes,default='M')
	color = models.CharField(max_length=10,choices=colors,default='White')
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return self.product.name + ' ' + self.size + ' ' + self.color

class BagItem(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bag")
	product_detail = models.ForeignKey(ProductDetail,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return self.user.username + ' ' + self.product_detail.product.name + ' ' + self.product_detail.color + ' ' + self.product_detail.size

class Coupon(models.Model):
	pattern = models.CharField(max_length=30)
	min_total_required = models.IntegerField()
	expiry = models.DateTimeField()
	is_percentage = models.BooleanField(default=True)
	amount = models.IntegerField()

class Order(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	address = models.ForeignKey(Address,models.SET_NULL,null = True)
	created = models.DateTimeField(auto_now_add = True)
	amount = models.IntegerField(default=0)
	coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True)


class OrderItem(models.Model):
	order = models.ForeignKey(Order,on_delete = models.CASCADE)
	product_detail = models.ForeignKey(ProductDetail,models.SET_NULL,null = True)
	quantity = models.IntegerField(default = 1)

class Wishlists(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	products = models.ForeignKey(Product,on_delete=models.CASCADE)

	def __str__(self):
		return self.products.name




