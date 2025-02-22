from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from datetime import date

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Add a valid email')
	
	class Meta:
		model = Account
		fields = ('email','username', 'password1','birth_date', 'password2','first_name','last_name','phone_number','sexe','wilaya','commune')

class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('username','password')
		
	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']

			if not authenticate(username=username, password=password):
				if not Account.objects.filter(email=username):
					raise forms.ValidationError('invalid login')
				else:
					if not authenticate(username=Account.objects.get(email=username),password=password):
						raise forms.ValidationError('invalid login')
