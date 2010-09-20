# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from hacklab.biblioteka.models import Book, Author
from hacklab.wrappers import render_to_response


# Views za gledanje na bibliotekata

def index(request):
	books = Book.objects.all()
	return render_to_response(request, 'biblioteka/list.html', {'knigi':books, 'heading':'Листа на сите книги во ХакЛаб КИКА'})

def view_kniga(request, k_id):
	book = get_object_or_404(Book, pk=k_id)
	tags = book.tags.split(', ')
	heading = '"'+ book.title + u'" од ' + u', '.join([a.name for a in book.authors.all()])
	return render_to_response(request, 'biblioteka/detali.html', {'kniga':book, 'heading':heading, 'tags':tags})

def by_godina(request, godina):
	books = Book.objects.filter(release_year=godina)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':books, 'heading':'Листа на сите книги од ' + str(godina) +' година'})

def by_tag(request, tag):
	books = Book.objects.filter(tags__contains=tag)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':books, 'heading':u'Листа на сите книги со клучен збор \"'+tag+'\"'})

def by_author(request, a_id):
	author = get_object_or_404(Author, pk=a_id)
	return render_to_response(request, 'biblioteka/list.html', {'knigi':author.book_set.all(), 'heading':u'Листа на сите книги од \"'+author.name+'\"'})


# views za naracuvanje i rezerviranje

def rezerviraj(request, k_id):
	'''
	Funkcija za rezerviranje na kniga od user-ot koj go pravi requestot
	'''
	return HttpResponse('sec')


def iznajmi(request, k_id, u_id):
	'''
	Funkcija za iznajmuvanje na kniga na user.
	requestot mora da se napravi od korisnik so issue permisija
	'''
	return HttpResponse('sec')
