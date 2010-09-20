from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from hacklab.registration.forms import RegistrationForm, EditAccountForm
from hacklab.registration.models import RegistrationProfile



def register(request, success_url='/registration/success/'):
	"""
	Allows a new user to register an account.

	"""
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = RegistrationProfile.objects.create_inactive_user(username=form.cleaned_data['username'],
																		password=form.cleaned_data['password1'],
																		email=form.cleaned_data['email'],
																		name=form.cleaned_data['first_name'],
																		surname=form.cleaned_data['last_name'])
			return HttpResponseRedirect(success_url)
	else:
		form = RegistrationForm()
	return render_to_response('registration/registration_form.html',
							  { 'form': form },
							  context_instance=RequestContext(request))



def edit_account(request):
	if request.method == 'POST':
		form = EditAccountForm(request.POST)
		if form.is_valid():
			u = User.objects.get(pk=request.user.id)
			# zemi gi novite podatoci od formata
			u.first_name = form.cleaned_data['first_name']
			u.last_name = form.cleaned_data['last_name']
			u.email = form.cleaned_data['email']
			# zacuvaj gi novite podatoci
			u.save()
	else:
		data = {
			'username':request.user.username,
			'first_name':request.user.first_name,
			'last_name':request.user.last_name,
			'email':request.user.email,
		}
		form = EditAccountForm(data)
	
	return render_to_response('account/edit_account.html', {'form':form}, context_instance=RequestContext(request))



