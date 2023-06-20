from django import forms
from django.forms import ModelForm
from .models import Product, Csv


class ProductForm (ModelForm):
	class Meta:
		model =Product
		fields = "__all__"
		widgets = { 
            'name': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Nama Product', 'required': True, } ),

        }

class CsvForm (forms.ModelForm):
	class Meta:
		model=Csv
		fields=['file_name',]