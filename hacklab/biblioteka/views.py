# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User

from hacklab.biblioteka.models import Book, Author, Rental, Publisher, Reservation
from hacklab.biblioteka.forms import RentalForm
from hacklab.wrappers import render_to_response



# Views za gledanje na bibliotekata

def index(request):
	'''
	Metod za listanje na site knigi 
	'''
	books = Book.objects.all()
	return render_to_response(request, 'biblioteka/list.html', {'knigi':books, 'heading':'Листа на сите книги во ХакЛаб КИКА'})


def view_kniga(request, k_id):
	'''
	Metod za gledanje na detali na odredena kniga
	'''
	book = get_object_or_404(Book, pk=k_id)
	tags = book.tags.split(', ')
	heading = '"'+ book.title + u'" од ' + u', '.join([a.name for a in book.authors.all()])
	return render_to_response(request, 'biblioteka/detali.html', {'kniga':book, 'heading':heading, 'tags':tags})


def by_godina(request, godina):
	'''
	Metod za listanje na site knigi od godina
	'''
	books = Book.objects.filter(release_year=godina)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':books, 'heading':'Листа на сите книги од ' + str(godina) +' година'})


def by_tag(request, tag):
	'''
	Metod za listanje na site knigi spored odbran tag
	'''
	books = Book.objects.filter(tags__contains=tag)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':books, 'heading':u'Листа на сите книги со клучен збор \"'+tag+'\"'})


def by_author(request, a_id):
	'''
	Metod za listanje na site knigi od avtor
	'''
	author = get_object_or_404(Author, pk=a_id)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':author.book_set.all(), 'heading':u'Листа на сите книги од \"'+author.name+'\"'})


def by_publisher(request, p_id):
	'''
	Metod za listanje na site knigi od izdavac
	'''
	publisher = get_object_or_404(Publisher, pk=p_id)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':publisher.book_set.all(), 'heading':u'Листа на сите книги од \"'+publisher.name+'\"'})


@permission_required('biblioteka.can_add_rental', login_url='/no_permission/')
def rezervirani(request):
	'''
	Metod za listanje na site rezervirani knigi.
	Potrebna e permisija
	'''
	reservations = Reservation.objects.filter(active=True)
	if request.method == 'POST':
		try:
			reservations = reservations.filter(book__ISBN=request.POST['ISBN'])
		except:
			pass
		
	return render_to_response(request, 'biblioteka/res_list.html', {'reservations':reservations, 'heading':'Листа на сите резервирани книги'})


# views za naracuvanje i rezerviranje
@login_required
def rezerviraj(request):
	'''
	Metod za rezerviranje na kniga od user-ot koj go pravi requestot
	'''
	#if request.session.__contains__('wishlist'):
		#wishlist = request.session.get('wishlist')
	#else:
		#wishlist = []
	if request.method == 'POST':
		kniga = get_object_or_404(Book, pk=request.POST['kniga'])
		try:
			# pri povik na index() metodot na python lista dokolku objektot go nema vo listata 
			# metodot frla exception ValueError, a dokolku go ima go vrakja indeksot od objektot
			#wishlist.index(kniga)
			reservation = get_object_or_404(Reservation, reserved_by=request.user, book=kniga, active=True)
		except Exception, e:
			# ako frli exception, odnosno ako go nema objektot vo listata, 
			# togas treba da se dodade vo baza
			#wishlist.append(kniga)
			Reservation.objects.create(book=kniga, reserved_by=request.user)
		# resetiranje na sesiskata promenliva
		#request.session.__setitem__('wishlist', wishlist)
	return HttpResponseRedirect('/biblioteka/cart/')


@permission_required('biblioteka.can_add_rental', login_url='/no_permission/')
def iznajmi(request, k_id):
	'''
	Metod za iznajmuvanje na kniga na user.
	requestot mora da se napravi od korisnik so can_add_rental permisija
	'''
	kniga = get_object_or_404(Book, pk=k_id)
	if request.method == 'POST':
		if kniga.in_stock > 0:
			# kreiranje na forma so podatocite zemeni od POST
			form = RentalForm(request.POST)
			if form.is_valid():
				# korisnikot na koj mu se iznajmuva knigata
				user = form.cleaned_data['user']
				# kreiranje i zacuvuvanje na nov objekt za izdavanje na kniga
				r = Rental.objects.create(book=kniga, rented_by=user)
				# se namaluva brojot na kopii vo bibliotekata
				kniga.in_stock -= 1
				kniga.save()
				return HttpResponseRedirect('/biblioteka/')
		else:
			return render_to_response(request, 'biblioteka/rent.html', {'heading':u'Изнајмувањето неможе да се изведе бидејќи нема преостанати копии.'})
	else:
		form = RentalForm()
	return render_to_response(request, 'biblioteka/rent.html', {'form':form, 'heading':u'Изнајмување на \"'+kniga.title+'\"'})



@permission_required('biblioteka.can_change_rental', login_url='/no_permission/')
def vrati(request, k_id):
	'''
	Metod za vrakjanje na rezervirana kniga
	'''
	# import na datetime za da se zapise vremeto na vrakjanje
	from datetime import datetime
	# ova ke treba da se smeni zosto user-ot koj go pravi requestot 
	# nemoze da vrakja bez da se proveri vrakjanjeto
	kniga = get_object_or_404(Book, pk=k_id)
	r = get_object_or_404(Rental, book=kniga, rented_by=request.user, returned_on=None)
	# se zapisuva vremeto na vrakjanje
	r.returned_on = datetime.now()
	r.save()
	# se pokacuva brojot na kopii vo bibliotekata
	kniga.in_stock += 1
	kniga.save()
	# vrakjanje na pocetnata strana
	return HttpResponseRedirect('/biblioteka/')



@login_required
def cart(request):
	wishlist = Book.objects.filter(reservation__active=True, reservation__reserved_by=request.user)
	return render_to_response(request, 'biblioteka/wishlist.html', {'knigi':wishlist, 'heading':u'Листа на сите мои резервирани книги'})



@login_required
def remove_from_cart(request):
	# request.session.__delitem__('wishlist')
	if request.method == 'POST':
		try:
			print request.POST['kniga']
			kniga = get_object_or_404(Book, pk=request.POST['kniga'])
			reservation = get_object_or_404(Reservation, reserved_by=request.user, book=kniga, active=True)
			reservation.active = False
			reservation.save()
		except Exception, exc:
			# ova stoi ovde za debug, 
			# koga ke se pravi deployment treba da se trgne i da se odkomentira redirektot
			# raise exc
			return HttpResponseRedirect('/biblioteka/')
	return HttpResponseRedirect('/biblioteka/cart/')


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
		rental_list = rental_list.filter(book__ISBN=ISBN)
	return rental_list.order_by('-rented_on')


@login_required
def history(request, rented_by=None, year=None, month=None):
	dates = Rental.objects.dates('rented_on', 'month')
	isbn = None
	if request.method == 'POST':
		try:
			isbn = request.POST['ISBN']
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


