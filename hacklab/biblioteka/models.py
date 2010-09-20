# -*- coding=utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from hacklab import settings



class Language(models.Model):
	name = models.CharField(max_length=20)
	iso_name = models.CharField(max_length=5)

	def __unicode__(self):
		return self.iso_name



class Author(models.Model):
	name = models.CharField(max_length=150)

	def __unicode__(self):
		return self.name



class Publisher(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name



class Book(models.Model):
	ISBN = models.CharField(max_length=30)
	title = models.CharField(max_length=250)
	release_year = models.IntegerField()
	lang = models.ForeignKey(Language)
	publisher = models.ForeignKey(Publisher)
	tags = models.CharField(max_length=300)
	authors = models.ManyToManyField(Author)
	description = models.CharField(max_length=500, null=True)
	image = models.ImageField(upload_to=settings.MEDIA_ROOT+'uploads/', null=True, blank=True)
	external_image_url = models.URLField(null=True, blank=True)
	quantity = models.IntegerField()
	in_stock = models.IntegerField()
	donated_by = models.CharField(max_length=128)

	def __unicode__(self):
		return self.title



class RentalManager(models.Manager):
	pass

class Rental(models.Model):
	book = models.ForeignKey(Book)
	rented_on = models.DateTimeField(auto_now_add=True)
	rented_by = models.ForeignKey(User)
	returned_on = models.DateTimeField(null=True)

	def __unicode__(self):
		return "%s rented to %s on %s" % (self.book.title, self.rented_by.username, self.rented_on)




class ReservationManager(models.Manager):
	pass

class Reservation(models.Model):
	book = models.ForeignKey(Book)
	reserved_by = models.ForeignKey(User, related_name="reservations")
	reserved_on = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)


	def __unicode__(self):
		return "%s reserved on %s by %s" % (self.book.title, self.reserved_on, self.reserved_by)



