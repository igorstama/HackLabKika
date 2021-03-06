from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
	'''
	Custom forma za registracija na korisnici.
	'''
	# ------ standardni polinja za user account 
	username = forms.CharField(label='Username', max_length=30)
	first_name = forms.CharField(label='First name', max_length=30)
	last_name = forms.CharField(label='Last name', max_length=30)
	email = forms.EmailField(label='email', max_length=75)
	password1 = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput)
	password2 = forms.CharField(label='Retype Password', max_length=20, widget=forms.PasswordInput)
	tos = forms.BooleanField()
	
	# funkcija za validacija na formata za vnesuvanje na nov korisnik 
	def clean(self):
		cleaned_data = self.cleaned_data
		passwd = [cleaned_data.get("password1"), cleaned_data.get("password2")]		
		if passwd[0] != passwd[1]:
			raise forms.ValidationError("Passwords must match !")
			message = u"Passwords must match !"
			self._errors["password1"] = ErrorList([message])
		return cleaned_data


	# validator funkcija koja proveruva dali ima User so vneseniot username
	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			# ako postoi raise exception
			u = User.objects.get(username=username)
			raise forms.ValidationError("User with the username \"%s\" already exists! Please enter a different username." % u.username)
		except User.DoesNotExist:
			# ako ne postoi, t.e. ako User.objects.get(username=username) 
			# frli exception User.DoesNotExist prodolzi uspesno
			pass	
		return self.cleaned_data['username']

	# validator funkcija koja proveruva dali ima User so vneseniot email
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			# ako postoi raise exception
			u = User.objects.get(email=email)
			raise forms.ValidationError("User with the email \"%s\" already exists! Please enter a different email." % u.email)
		except User.DoesNotExist:
			# ako ne postoi, t.e. ako User.objects.get(username=username) 
			# frli exception User.DoesNotExist prodolzi uspesno
			pass	
		return self.cleaned_data['email']


class EditAccountForm(forms.Form):
	first_name = forms.CharField(label='First name', max_length=30)
	last_name = forms.CharField(label='Last name', max_length=30)
	email = forms.EmailField(label='email', max_length=75)





