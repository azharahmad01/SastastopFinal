from django.shortcuts import render
from django.views.generic.base import TemplateView
from product.models import Product
# Create your views here.

class HomeView(TemplateView):
	template_name="home/home.html"

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['products'] = Product.objects.all()[:11]
		return context

