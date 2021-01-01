from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from django import forms


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60)
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)

	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email','password1','password2']


class UserUpdateForm(UserChangeForm):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	img = forms.ImageField()
	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','img']