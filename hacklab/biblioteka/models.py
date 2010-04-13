from django.db import models
from django.contrib.auth.models import User


LANGUAGES = (
	('MK', 'Makedonski'),
	('EN', 'Angliski'),
	('SRB','Srpski'),
	('CRO', 'Hrvatski'),
	('DE', 'Germanski'),
	('FR', 'Francuski'),
	('ES', 'Spanski'),
	('ND', 'Holandski'),
	('FI', 'Finski'),
	('SW', 'Svedski'),
)

class Author(models.Model):
	name = models.CharField(max_length=150)

	def __unicode__(self):
		return self.name



class Book(models.Model):
	title = models.CharField(max_length=250)
	ISBN = models.CharField(max_length=30)
	release_year = models.IntegerField()
	lang = models.CharField(max_length=20, choices=LANGUAGES)
	tags = models.CharField(max_length=300)
	authors = models.ManyToManyField(Author)
	description = models.CharField(max_length=500, null=True)
	
	def __unicode__(self):
		return self.title



class Rental(models.Model):
	book = models.ForeignKey(Book)
	rentedon = models.DateTimeField(auto_now_add=True)
	returned_on = models.DateTimeField()
	rented_from = models.ForeignKey(User)
	
	def __unicode__(self):
		return "%s - %s %s-:-%s" % (self.book.title, self.rented_from.username, self.rented_on, self.returned_on)



class Reservation(models.Model):
	reserved_on = models.DateTimeField(auto_now_add=True)
	reserved_from = models.ForeignKey(User)
	book = models.ForeignKey(Book)

