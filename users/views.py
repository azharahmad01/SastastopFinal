from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomRegistrationForm, AddressForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import (
	ListView,
	CreateView,
	UpdateView,
	)

from .models import Address 
from product.models import Wishlists
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.

app_name =  "user"

class ProfileView(LoginRequiredMixin,TemplateView):
	template_name="users/profile.html"


@login_required
def ProfileDetails(request):
	return render(request,'users/profile_page.html')


@login_required
def ProfileEdit(request):
	if request.method=="POST":
		u_form= UserUpdateForm(request.POST,instance=request.user)
		p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Your account has been updated!')
            
			return redirect('profile') 
	else:
		u_form= UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(instance=request.user.profile)
	context={
        'u_form':u_form,
        'p_form':p_form
    }
	return render(request,'users/profile-edit.html',context)


@login_required
def createAddressView(request):
	if request.method == 'POST':
		form = AddressForm(request.POST)
		if form.is_valid():
			address = form.save()
			address.users.add(request.user)
			address.save()
			return redirect('addresses')

	form = AddressForm()
	context = {
	'form':form,
	'addresses':request.user.addresses.all()
	}
	return render(request,'users/addresses.html',context)

@login_required
def AddressView(request):
	form = AddressForm()
	context = {
	'form':form,
	'addresses':request.user.addresses.all()
	}
	return render(request,'users/addresses.html',context)


@login_required
def deleteAddressView(request,pk):
	address = get_object_or_404(Address,id=pk)
	address.delete()

	return redirect('addresses')

@login_required
def getUpdateFormView(request,pk):
	address = get_object_or_404(Address,id=pk)
	form = AddressForm(instance = address)

	context = {
	'u_form':form,
	'address_id':pk,
	'addresses':request.user.addresses.all()
	}
	return render(request,'users/addresses.html',context)

@login_required
def UpdateAddressFormView(request,pk):
	address = get_object_or_404(Address,id=pk)
	form = AddressForm(request.POST,instance = address)
	if form.is_valid():
		form.save()
		messages.success(request,f'Your address has been Updated!!')
		return redirect('addresses')



def register(request):
    form = CustomRegistrationForm()

    if request.method == 'POST':
        # Sign up
        if request.POST.get('submit') == 'sign_up':
            form = CustomRegistrationForm(
                request.POST or None, request.FILES or None)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                form.save()
                return redirect('account-registration')
        # end signup
        #---------------------------------------------------#
        # signin

        if request.POST.get('submit') == 'sign_in':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f'Welome {user.username}! Happy shopping!!')
                return redirect('home')
            else:
                messages.error(request, f'Username Or Password is incorrect')

        # signin end
        #----------------------------------------------------#
    context = {'form': form}
    return render(request, 'users/Register.html', context)


# logout
@login_required
def logOutUser(request):
    logout(request)
    messages.info(
        request, f'Successfully LoggedOut!! Keep Shopping with Us!!')
    return redirect('account-registration')

@login_required
def wishlist_view(request):
	products = Wishlists.objects.filter(user=request.user)
	context = {"products":products, "numProducts":products.count()}
	return render(request,'users/wishlist.html',context)


