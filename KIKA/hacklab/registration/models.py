from django.db import models

import datetime, random, re, hashlib
from django.db import models
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings




class RegistrationManager(models.Manager):
	"""
	Custom manager for the RegistrationProfile model.
	
	"""
	def create_inactive_user(self, name, surname, username, password, email):
		"""
		Creates a new User and a new RegistrationProfile for that User
		"""
		
		# Create the user.
		new_user = User.objects.create_user(username, email, password)
		new_user.first_name = name
		new_user.last_name = surname
		new_user.is_active = False
		new_user.save()
                
		return new_user


class RegistrationProfile(models.Model):
	# napraven e model za ponatamosno koristenje i dopolnuvanje
	# sega za sega nema sto da se stavi ovde osven managerot
	objects = RegistrationManager()