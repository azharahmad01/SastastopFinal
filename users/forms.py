from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Address, Profile


class CustomRegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email','password1','password2']




class AddressForm(forms.ModelForm):
	address1 = forms.CharField(widget=forms.Textarea())
	address2 = forms.CharField(widget=forms.Textarea())
	class Meta:
		model = Address 
		fields = ['name','address1', 'address2', 'postcode', 'city', 'phone']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    # gender = forms.ChoiceField(widget=fo())
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'phone', 'birth_date']
