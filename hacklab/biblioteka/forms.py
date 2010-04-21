# -*- coding=utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from hacklab.biblioteka.models import Rental


class RentalForm(forms.Form):
	user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, label="Корисник кој ја изнајмува книгата")

