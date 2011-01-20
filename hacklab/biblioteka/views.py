# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from hacklab.biblioteka.models import Book, Author, Rental, Publisher, Reservation, ReservationExists, RentalExists
from hacklab.biblioteka.forms import RentalForm
from hacklab.wrappers import render_to_response



# Views za gledanje na bibliotekata

def index(request):
	"""
	Metod za listanje na site knigi
	"""
	books = Book.objects.all()
	return render_to_response(request, 'biblioteka/list.html',
			{'knigi':books, 'heading':'Листа на сите книги во ХакЛаб КИКА'})


def view_book_details(request, k_id):
	"""
	Metod za gledanje na detali na odredena kniga
	"""
	book = get_object_or_404(Book, pk=k_id)
	tags = book.tags.split(', ')
	heading = '"'+ book.title + u'" од ' + u', '.join([a.name for a in book.authors.all()])
	return render_to_response(request, 'biblioteka/detali.html',
			{'kniga':book, 'heading':heading, 'tags':tags})


def by_year(request, godina):
	"""
	Metod za listanje na site knigi od godina
	"""
	books = Book.objects.filter(release_year=godina)
	return render_to_response(request, 'biblioteka/list.html',
			{'knigi':books, 'heading':'Листа на сите книги од ' + str(godina) +' година'})


def by_tag(request, tag):
	"""
	Metod za listanje na site knigi spored odbran tag
	"""
	books = Book.objects.filter(tags__contains=tag)
	return render_to_response(request, 'biblioteka/list.html',
			{'knigi':books, 'heading':u'Листа на сите книги со клучен збор \"'+tag+'\"'})


def by_author(request, a_id):
	"""
	Metod za listanje na site knigi od avtor
	"""
	author = get_object_or_404(Author, pk=a_id)
	return render_to_response(request, 'biblioteka/list.html',
			{'knigi':author.book_set.all(), 'heading':u'Листа на сите книги од \"'+author.name+'\"'})


def by_publisher(request, p_id):
	"""
	Metod za listanje na site knigi od izdavac
	"""
	publisher = get_object_or_404(Publisher, pk=p_id)
	return render_to_response(request, 'biblioteka/list.html',
			{'knigi':publisher.book_set.all(), 'heading':u'Листа на сите книги од \"'+publisher.name+'\"'})


@permission_required('biblioteka.can_add_rental', login_url=settings.LOGIN_URL)
def reserved_books(request):
	"""
	Metod za listanje na site rezervirani knigi.
	Potrebna e permisija za dodavanje na rental.
	"""
	reservations = Reservation.objects.filter(active=True)
	if request.method == 'POST':
		try:
			reservations = reservations.filter(book__ISBN=request.POST['ISBN'])
		except:
			pass

	return render_to_response(request, 'biblioteka/res_list.html',
			{'reservations':reservations, 'heading':'Листа на сите резервирани книги'})


@login_required
def reserve_book(request):
	"""
	Metod za rezerviranje na kniga od user-ot koj go pravi requestot.
	"""
	if request.method == 'POST':
		try:
			kniga = get_object_or_404(Book, pk=request.POST['kniga'])
			kniga.reserve_to(request.user)
		except ReservationExists:
			pass
	return HttpResponseRedirect(reverse('hacklab.biblioteka.views.cart'))


@login_required
@permission_required('biblioteka.can_add_rental', login_url=settings.LOGIN_URL)
def rent_book(request, k_id):
	"""
	Metod za iznajmuvanje na kniga na user.
	requestot mora da se napravi od korisnik so can_add_rental permisija
	"""
	kniga = get_object_or_404(Book, pk=k_id)
	if request.method == 'POST':
		if kniga.in_stock > 0:
			# kreiranje na forma so podatocite zemeni od POST
			form = RentalForm(request.POST)
			if form.is_valid():
				# korisnikot na koj mu se iznajmuva knigata
				user = form.cleaned_data['user']
				kniga.rent_to(user)
				return HttpResponseRedirect(reverse('hacklab.biblioteka.views.index'))
		else:
			h = u'Изнајмувањето неможе да се изведе бидејќи нема преостанати копии.'
			return render_to_response(request, 'biblioteka/rent.html', {'heading':h})
	else:
		form = RentalForm()
		field = form.fields['user']
		qs = User.objects.exclude(rental__book=kniga, rental__returned_on=None)

		if qs.count() > 0:
			field.queryset = qs
	return render_to_response(request, 'biblioteka/rent.html',
			{'form':form, 'heading':u'Изнајмување на \"'+kniga.title+'\"'})


@login_required
@permission_required('biblioteka.can_change_rental')
def return_book(request, k_id):
	"""
	Metod za vrakjanje na rezervirana kniga
	"""
	# import na datetime za da se zapise vremeto na vrakjanje
	from datetime import datetime
	kniga = get_object_or_404(Book, pk=k_id)
	# zemanje na site korisnici koi ja imaat iznajmeno knigata (ako ima poveke kopii)
	users = User.objects.filter(rental__book=kniga, rental__returned_on=None)

	if request.method=="POST":
		# kreiranje na forma so podatocite zemeni od POST
		form = RentalForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data['user']
			kniga.return_by(user)
	else:
		form = RentalForm()
		qs = User.objects.filter(rental__book=kniga, rental__returned_on=None)

		if qs.count() > 0:
			field = form.fields['user']
			field.queryset = qs
		return render_to_response(request, 'biblioteka/return.html', {'kniga':kniga, 'form':form})
	return HttpResponseRedirect(reverse('hacklab.biblioteka.views.index'))



@login_required
def cart(request):
	wishlist = Reservation.objects.filter(active=True, reserved_by=request.user)
	return render_to_response(request, 'biblioteka/wishlist.html', {'reservations':wishlist,
								'heading':u'Листа на сите резервирани книги'})



@login_required
def remove_from_cart(request):
	# request.session.__delitem__('wishlist')
	if request.method == 'POST':
		try:
			reservation = get_object_or_404(Reservation, pk=request.POST['reservation'])
			reservation.delete()
			# reservation.save()
		except Exception, exc:
			# ova stoi ovde za debug,
			# koga ke se pravi deployment treba da se trgne dolnava linija
			# i da se dodade custom 500 (server error) handler
			print "EXCEPTION ======== %s" % exc
	return HttpResponseRedirect(reverse('hacklab.biblioteka.views.cart'))


def get_rental_list(user=None, year=None, month=None, ISBN=None):
	if user is not None:
		rental_list = Rental.objects.filter(rented_by=user)
	else:
		rental_list = Rental.objects.all()
	if year is not None:
		rental_list = rental_list.filter(rented_on__year=year)
	if month is not None:
		rental_list = rental_list.filter(rented_on__month=month)
	if ISBN is not None:
		rental_list = rental_list.filter(book__ISBN=ISBN.strip())
	return rental_list.order_by('-rented_on')


@login_required
def history(request, rented_by=None, year=None, month=None):
	dates = Rental.objects.dates('rented_on', 'month')
	isbn = None
	if request.method == 'POST':
		try:
			isbn = request.POST['ISBN'].strip()
		except:
			pass

	if rented_by is None:
		if request.user.has_perm('can_add_rental'):
			rental_list = get_rental_list(year=year, month=month, ISBN=isbn)
		else:
			rental_list = get_rental_list(user=request.user, year=year, month=month, ISBN=isbn)
	else:
		rental_list = get_rental_list(user=rented_by, year=year, month=month, ISBN=isbn)
	path = "/".join(request.path.split('/')[1:3])
	return render_to_response(request, 'biblioteka/history.html', {'list':rental_list, 'dates':dates, 'path':path})


@login_required
def my_history(request, year=None, month=None):
	return history(request, rented_by=request.user, year=year, month=month)


