from django import forms
from django.forms import ModelForm
from .models import ListData, EntryData, CSV
from product.models import Product

class AddListForm (ModelForm):
	class Meta:
		model =ListData
		fields = "__all__"
		widgets = { 
            'nama_list': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Nama List', 'required': True, } ),

        }

class AddEntryData (ModelForm):
	product= forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
	class Meta:
		model = EntryData
		fields = ('product', 'kuantitas_terjual', 'jumlah_transaksi', 'produk_rusak', 'sisa_produk','stok_awal', 'stok_akhir', 'hari_periode' )
		widgets = {
        'product': forms.Select(attrs={'class': 'custom-select'}),
        'kuantitas_terjual': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Kuantitas Terjual', 'required': True, } ),
        'jumlah_transaksi': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Jumlah Transaksi', 'required': True, } ),       
        'produk_rusak': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Produk Rusak', 'required': True, } ),            
        'sisa_produk': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Sisa Produk', 'required': True, } ),
        'stok_awal': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Persediaan Awal Periode', 'required': True, } ),
        'stok_akhir': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Persediaan Akhir Periode', 'required': True, } ),
        'hari_periode': forms.TextInput( attrs={ 'class': 'form-control validate', 'placeholder': 'Hari Periode', 'required': True, } ),
        }


class CsvForm (forms.ModelForm):
	class Meta:
		model=CSV
		fields=['file_name',]

