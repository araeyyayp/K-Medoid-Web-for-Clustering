from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import csv
import xlwt


# Create your views here.


def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
	    if request.method == 'POST':
	        form = UserRegisterForm(request.POST)
	        if form.is_valid():
	           form.save()
	           username = form.cleaned_data.get('username')
	           email = form.cleaned_data.get('email')
	           messages.success(request, 'Your account has been created!')
	           return redirect('account:login')
	    else:
	        form = UserRegisterForm()
	    context = {
	        'form': form
	        }
	    return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('account:homepage')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('account:homepage')
			else:
				messages.error(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('account:login')

@login_required(login_url='account:login')
def home(request):
	context ={
		'judul' : 'Home Beranda'
	}

	return render (request, 'accounts/index.html', context)

@login_required(login_url='account:login')
def homepage(request):
	context ={
		'judul' : 'Home Beranda'

	}

	return render (request, 'homepage.html', context)

@login_required(login_url='account:login')
def export_excel (request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="templatefileexcelperiode.csv"'

	style = xlwt.XFStyle()

	wb=csv.writer(response)
	wb.writerow(['product','kuantitas_terjual','jumlah_transaksi','produk_rusak','sisa_produk','stok_awal','stok_akhir','hari_periode'])
	wb.writerow(['OBH Anak Straw 55 ml','527','7351933','0','275','419','0','365'])

	return response

@login_required(login_url='account:login')
def export_xls (request):

	response = HttpResponse(content_type='text/xls')
	response['Content-Disposition'] = 'attachment; filename="templatefileexcelperiode.xls"'

	style = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',
    	num_format_str='#,##0.00')
	# Workbook is created
	wb = xlwt.Workbook()

	  
	# add_sheet is used to create sheet.
	sheet1 = wb.add_sheet('Sheet 1')
	  
	sheet1.write(0, 0, 'product', style)
	sheet1.write(1, 0, 'OBH Anak Straw 55 ml', style)
	sheet1.write(0, 1, 'kuantitas_terjual', style)
	sheet1.write(1, 1, '527', style)
	sheet1.write(0, 2, 'jumlah_transaksi,,,,,', style)	
	sheet1.write(1, 2, '7351933', style)
	sheet1.write(0, 3, 'produk_rusak', style)
	sheet1.write(1, 3, '0', style)
	sheet1.write(0, 4, 'sisa_produk', style)
	sheet1.write(1, 4, '275', style)
	sheet1.write(0, 5, 'stok_awal', style)
	sheet1.write(1, 5, '419', style)
	sheet1.write(0, 6, 'stok_akhir', style)
	sheet1.write(1, 6, '0', style)
	sheet1.write(0, 7, 'hari_periode', style)
	sheet1.write(1, 7, '365', style)
	  
	wb.save(response)
	return response

@login_required(login_url='account:login')
def export_excel_tahun (request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="templatefileexceltahun.csv"'

	style = xlwt.XFStyle()

	wb=csv.writer(response)
	wb.writerow(['product','kuantitas_terjual','jumlah_transaksi','produk_rusak','sisa_produk','stok_awal','stok_akhir'])
	wb.writerow(['OBH Anak Straw 55 ml','527','7351933','0','275','419','0'])

	return response

@login_required(login_url='account:login')
def export_xls_tahun (request):

	response = HttpResponse(content_type='text/xls')
	response['Content-Disposition'] = 'attachment; filename="templatefileexceltahun.xls"'

	style = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',
    	num_format_str='#,##0.00')
	# Workbook is created
	wb = xlwt.Workbook()

	  
	# add_sheet is used to create sheet.
	sheet1 = wb.add_sheet('Sheet 1')
	  
	sheet1.write(0, 0, 'product', style)
	sheet1.write(1, 0, 'OBH Anak Straw 55 ml', style)
	sheet1.write(0, 1, 'kuantitas_terjual', style)
	sheet1.write(1, 1, '527', style)
	sheet1.write(0, 2, 'jumlah_transaksi,,,,,', style)	
	sheet1.write(1, 2, '7351933', style)
	sheet1.write(0, 3, 'produk_rusak', style)
	sheet1.write(1, 3, '0', style)
	sheet1.write(0, 4, 'sisa_produk', style)
	sheet1.write(1, 4, '275', style)
	sheet1.write(0, 5, 'stok_awal', style)
	sheet1.write(1, 5, '419', style)
	sheet1.write(0, 6, 'stok_akhir', style)
	sheet1.write(1, 6, '0', style)

	  
	wb.save(response)
	return response

@login_required(login_url='account:login')
def export_excel_produk (request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="templatefileexceltahun.csv"'

	style = xlwt.XFStyle()

	wb=csv.writer(response)
	wb.writerow(['product'])
	wb.writerow(['OBH Anak Straw 55 ml'])

	return response

@login_required(login_url='account:login')
def export_xls_produk (request):

	response = HttpResponse(content_type='text/xls')
	response['Content-Disposition'] = 'attachment; filename="templatefileexceltahun.xls"'

	style = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',
    	num_format_str='#,##0.00')
	# Workbook is created
	wb = xlwt.Workbook()

	  
	# add_sheet is used to create sheet.
	sheet1 = wb.add_sheet('Sheet 1')
	  
	sheet1.write(0, 0, 'product', style)
	sheet1.write(1, 0, 'OBH Anak Straw 55 ml', style)


	  
	wb.save(response)
	return response