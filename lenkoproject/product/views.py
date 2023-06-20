from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from .models import Product, Csv
from .forms import ProductForm, CsvForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import csv
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='account:login')
def producthome(request):
	context ={
		'judul' : 'Product Data Home'
	}

	return render (request, 'product/producthome.html', context)

@login_required(login_url='account:login')
def addproduct(request):
	submitted = False
	if request.method =="POST":
		form= ProductForm (request.POST)
		if form.is_valid():
			form.save()
			productname = form.cleaned_data.get('productname')
			return HttpResponseRedirect('/product/list')
	else:
		form= ProductForm
		if 'submitted' in request.GET:
			submitted=True

	return render (request, 'product/tambahproduct.html', {'form':form, 'submitted': submitted })


class ProductView(ListView):
	model= Product
	template_name= 'product/productlist.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['num_product'] = Product.objects.all().count()
		return context


@login_required(login_url='account:login')
def deleteproduct (request,pk):
	product= Product.objects.filter(id=pk).last()
	product.delete()
	return redirect ('product:list')

@login_required(login_url='account:login')
def editproduct(request, pk):

	productlist = Product.objects.get(id=pk)


	form= ProductForm(instance=productlist)

	if request.method =="POST":
		form= ProductForm (request.POST, instance=productlist)
		if form.is_valid():
			form.save()
			return redirect ('product:list')
		else:
			print ('FORM IS INVALID')
	
	else:

		form=ProductForm(instance=productlist)


	context = {
		'form' : form,
		'listdata' : productlist
	}

	return render (request, "product/editproduct.html", context)

@login_required(login_url='account:login')
def uploadproduct(request):

	error_message=None
	success_message=None

	form = CsvForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		form= CsvForm()

		try:

			obj= Csv.objects.get(activated=False)
			product = []
			with open (obj.file_name.path, 'r') as f:
				reader = csv.reader(f, delimiter=",")
				for row in reader:
					product.append(row)

			labels = product.pop(0)
			print(labels)
			print(product)
			print (obj.id)

			for row in product:
				Product.objects.create(
					name= row[0],
						)

               

			obj.activated=True
			obj.save()
			success_message= "Upload Success"
        
		except:
			error_message= "Something went wrong..."



	context = {
		'form': form,
		'success_message': success_message,
		'error_message' : error_message,

    }
	return render(request, 'product/uploadproduct.html', context)