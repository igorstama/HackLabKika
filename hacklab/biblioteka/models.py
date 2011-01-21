#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from hacklab import settings
from datetime import datetime


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


class BookNotInStock(Exception):
	pass

class ReservationExists(Exception):
	pass

class RentalExists(Exception):
	pass


class Book(models.Model):
	ISBN = models.CharField(max_length=30)
	title = models.CharField(max_length=250)
	release_year = models.IntegerField(null=True, blank=True)
	lang = models.ForeignKey(Language, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	tags = models.CharField(max_length=300, null=True, blank=True)
	authors = models.ManyToManyField(Author)
	description = models.CharField(max_length=500, null=True)
	image = models.ImageField(upload_to=settings.MEDIA_ROOT+'uploads/', null=True, blank=True)
	external_image_url = models.URLField(null=True, blank=True)
	quantity = models.IntegerField(default=1)
	in_stock = models.IntegerField(default=1)
	donated_by = models.CharField(max_length=128, null=True, blank=True)

	def __unicode__(self):
		return self.title

	def rent_to(self, user):
		"""
		Method for renting books.
		First it checks if the book is in stock, if so, it then checks
		for an active rental by the user on the book.
		"""
		if self.quantity > 0:
			# get rental on this book by the user
			r = Rental.active_objects.get_rental(user, self)
			if r is None:
				# if there is none create a new rental
				r = Rental.objects.create(book=self, rented_by=user)
				r.save()
				# remove the reservation if it exists
				self.remove_reservation(user)
				self.in_stock += 1
				self.save()
			else:
				# if there is a rental by the user, raise a custom exception
				raise RentalExists("Book %s is already rented by user %s" % (self.title, user.username))
		else:
			# if the book isn't in stock raise a custom exception
			raise BookNotInStock("Book %s can't be rented because it's out of stock!" % self.title)

	def return_by(self, user):
		"""
		Method for returning books.
		"""
		r = Rental.active_objects.get_rental(user, self)
		if r is None:
			raise Rental.DoesNotExist
		else:
			r.returned_on = datetime.now()
			r.save()
			self.in_stock += 1
			self.save()

	def reserve_to(self, user):
		"""
		Function for making a reservation on this book by the given user.
		If the reservation exists an exception is raised.
		"""
		reservation = Reservation.active_objects.get_reservation(user, self)
		if reservation is None:
			reservation = Reservation.objects.create(book=self, reserved_by=user)
			reservation.save()
		else:
			raise ReservationExists("User %s has an active reservation on %s" % (user.username, self.title))

	def remove_reservation(self, user):
		"""
		Function for removing a reservation by the user.
		"""
		try: # if the reservation exists remove it
			reservation = Reservation.active_objects.get(reserved_by=user, book=self)
			reservation.delete()
		except Reservation.DoesNotExist: # else die quetly
			pass



class ActiveRentalManager(models.Manager):
	"""
	Manager for active rentals (Not yet returned).
	"""
	def get_query_set(self):
		return super(ActiveRentalManager, self).get_query_set().filter(returned_on=None)

	def get_rental(self, user, book):
		try:
			rental = self.get(rented_by=user, book=book)
			return rental
		except Rental.DoesNotExist:
			return None


class Rental(models.Model):
	book = models.ForeignKey(Book)
	rented_on = models.DateTimeField(auto_now_add=True)
	rented_by = models.ForeignKey(User)
	returned_on = models.DateTimeField(null=True)

	objects = models.Manager()
	active_objects = ActiveRentalManager()

	def __unicode__(self):
		return "%s rented to %s on %s" % (self.book.title, self.rented_by.username, self.rented_on)


class ActiveReservationManager(models.Manager):
	"""
	Manager for the active reservations
	"""
	def get_query_set(self):
		return super(ActiveReservationManager, self).get_query_set().filter(active=True)

	def get_reservation(self, user, book):
		"""
		Method that checks for a given reservation.
		If exists the reservation is returned,
		else None is returned
		"""
		try:
			reservation = self.get(reserved_by=user, book=book)
			return reservation
		except Reservation.DoesNotExist:
			return None


class Reservation(models.Model):
	book = models.ForeignKey(Book)
	reserved_by = models.ForeignKey(User, related_name="reservations")
	reserved_on = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = models.Manager()
	active_objects = ActiveReservationManager()

	def __unicode__(self):
		return "%s reserved on %s by %s" % (self.book.title, self.reserved_on, self.reserved_by)



