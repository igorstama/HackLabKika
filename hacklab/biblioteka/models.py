#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime


class Language(models.Model):
    name = models.CharField("Назив", max_length=20)
    iso_name = models.CharField("ISO-2 Кратенка", max_length=5)

    def __unicode__(self):
        return self.iso_name


class Author(models.Model):
    name = models.CharField("Назив", max_length=150, help_text="Име и презиме на авторот")

    def __unicode__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField("Назив", max_length=30, help_text="Назив на издавачот")

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
    title = models.CharField("Наслов", max_length=250, help_text="Наслов на книгата")
    release_year = models.IntegerField("Година", null=True, blank=True, help_text="Година на издавање")
    lang = models.ForeignKey(Language, null=True, blank=True, help_text="Јазик")
    publisher = models.ForeignKey(Publisher, null=True, blank=True, help_text="Издавач на книгата")
    tags = models.CharField("Тагови", max_length=300, null=True, blank=True, help_text="Сепаратор=запирка(,)")
    authors = models.ManyToManyField(Author, help_text="Авотри на книгата")
    description = models.CharField("Опис", max_length=500, null=True, blank=True, help_text="краток опис на книгата")
    image = models.ImageField("Слика", upload_to=settings.MEDIA_ROOT+'uploads/', null=True, blank=True, help_text="")
    external_image_url = models.URLField("Надворешна слика", null=True, blank=True, help_text="Слика која ќе се чува на серверот")
    quantity = models.IntegerField("Количина", default=1, help_text="Вкупна количина на книги")
    in_stock = models.IntegerField("Преостанати копии", default=1, help_text="Колку вкупно копии има преостанато во библиотеката")
    donated_by = models.CharField("Донирана од", max_length=128, null=True, blank=True, help_text="Од кого е донирана книгата")

    def __unicode__(self):
        return self.title


class ActiveRentalManager(models.Manager):
    """
    Manager for active rentals (Not yet returned).
    """
    def get_query_set(self):
        return super(ActiveRentalManager, self).get_query_set().filter(returned_on=None)

    def get_rental(self, user, book):
        return self.get(rented_by=user, book=book)

    def return_book(self, user, book):
        """
        Method for returning books.
        """
        r = self.get_rental(user, book)
        r.returned_on = datetime.now()
        r.save()
        r.book.in_stock += 1
        r.book.save()

    def rent_book(self, user, book):
        """
        Method for renting books.
        First it checks if the book is in stock, if so, it then checks
        for an active rental by the user on the book.
        """
        if book.in_stock > 0:
            # get rental on this book by the user
            try:
                r = self.get_rental(user, book)
                # if there is a rental by the user, raise a custom exception
                raise RentalExists("Book %s is already rented by %s" % (book.title, user.username))
            except Rental.DoesNotExist:
                # if there is none create a new rental
                r = Rental.objects.create(book=book, rented_by=user)
                r.save()
                # remove the reservation if it exists
                Reservation.objects.remove_reservation(user, book)
                book.in_stock -= 1
                book.save()
        else:
            # if the book isn't in stock raise a custom exception
            raise BookNotInStock("Book %s is out of stock!" % book.title)

class Rental(models.Model):
    book = models.ForeignKey(Book)
    rented_on = models.DateTimeField(auto_now_add=True)
    rented_by = models.ForeignKey(User)
    returned_on = models.DateTimeField(null=True)

    objects = models.Manager()
    active_objects = ActiveRentalManager()

    def __unicode__(self):
        return "%s rented by %s on %s" % (self.book.title, self.rented_by.username, self.rented_on)


class ReservationManager(models.Manager):
    """
    Manager for the active reservations
    """
    def get_query_set(self):
        return super(ReservationManager, self).get_query_set().filter(active=True)

    def remove_reservation(self, r_id=None, user=None, book=None):
        """
        Function for removing a reservation by the user.
        """
        try: # if the reservation exists remove it
            if user is not None:
                reservation = self.get(reserved_by=user, book=book)
            reservation = self.get(pk=r_id)
            reservation.delete()
        except Reservation.DoesNotExist: # else die quetly
            pass


class Reservation(models.Model):
    book = models.ForeignKey(Book)
    reserved_by = models.ForeignKey(User, related_name="reservations")
    reserved_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = ReservationManager()

    def __unicode__(self):
        return "%s reserved on %s by %s" % (self.book.title, self.reserved_on, self.reserved_by)

    def save(self, *args, **kwargs):
        try: # if the reservation exists remove it
            r = Reservation.objects.get(reserved_by=self.reserved_by, book=self.book, active=True)
            raise ReservationExists("User %s has an active reservation on %s" %
                    (self.reserved_by.username, self.book.title))
        except Reservation.DoesNotExist:
            super(Reservation, self).save(*args, **kwargs)


