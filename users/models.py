from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Address(models.Model):
	name = models.CharField(max_length=80,default='USER')
	users = models.ManyToManyField(User,related_name="addresses")
	address1 = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100)
	postcode = models.CharField(max_length=6)
	city = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)

	def __str__(self):
		return self.address1
	

class UserManager(models.Manager):
	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_ND = 2
	GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'),(GENDER_ND,'not defined')]
	def males(self):
		return self.all().filter(gender=self.GENDER_MALE)
	def females(self):return self.all().filter(gender=self.GENDER_FEMALE)
	def notdefined(self):return self.all().filter(gender=self.GENDER_ND)

class Profile(models.Model):
	#user
	user =  models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile') 
	 
    #imagefield
	image = models.ImageField(default='default.jpg' , upload_to = 'profile_pics')
	birth_date = models.DateField(null=True, blank=True)
    
	#gender
	gender=models.IntegerField(choices=UserManager.GENDER_CHOICES,default=UserManager.GENDER_ND)
	phone = models.CharField(max_length=10)

	def __str__(self):
		return f'{self.user.username} Profile'

	def greet(self):
		return {UserManager.GENDER_MALE:'Hi, boy', UserManager.GENDER_FEMALE:'Hi, girl.'}[self.gender]


	



	


