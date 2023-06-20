from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from .models import ListData, EntryData, CSV
from .forms import AddListForm, AddEntryData, CsvForm
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import csv
import xlwt
from product.models import Product
from django.core.files.base import ContentFile
import pandas as pd
import numpy as np
import json
import os
from django.conf import settings
from array import *
from scipy.stats import zscore
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score
from sklearn import cluster, datasets, preprocessing, metrics
from sklearn import metrics
from .utils import get_graph, get_plot, get_plot2, try_get_plot, try_get_plot2, try_get_plot3
from scipy import stats
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from io import StringIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import reportlab.lib, reportlab.platypus
import os
from adminprofiles.models import AdminProfile
from report.models import Report, Report2, Report3
import ast
import base64
from report.forms import PdfForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required



# Create your views here.


class ListDataView(ListView):
	model= ListData
	template_name= 'inventdata/inventdatalist.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['listnum'] = ListData.objects.all().count()
		return context

@login_required(login_url='account:login')
def deletelist (request,pk):
	product= ListData.objects.filter(id=pk).last()
	product.delete()
	return redirect ('inventdata:list')

@login_required(login_url='account:login')
def editlist(request, pk):

	listlist = ListData.objects.get(id=pk)


	form= AddListForm(instance=listlist)

	if request.method =="POST":
		form= AddListForm (request.POST, instance=listlist)
		if form.is_valid():
			form.save()
			return redirect ('inventdata:list')
		else:
			print ('FORM IS INVALID')
	
	else:

		form=AddListForm(instance=listlist)


	context = {
		'form' : form
	}

	return render (request, "inventdata/editlist.html", context)


class ListDetailView(DetailView):
	model = ListData
	template_name= 'inventdata/detaillist.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk = self.kwargs["pk"]

		form = AddEntryData()
		listdata = get_object_or_404(ListData, pk=pk)
		entrydata = listdata.entrydata_set.all()

		context['listdata'] = listdata
		context['entrydata'] = entrydata
		context['form'] = form
		return context

	def listdata(self, request, *args, **kwargs):
		form = AddEntryData(request.POST)
		self.object = self.get_object()
		context = super().get_context_data(**kwargs)

		listdata = ListData.objects.filter(id=self.kwargs['pk'])[0]
		entrydata = listdata.entrydata_set.all()

		context['listdata'] = listadata
		context['entrydata'] = entrydata
		context['form'] = form

		if form.is_valid():
			product = form.cleaned_data['product']
			kuantitas_terjual = form.cleaned_data['kuantitas_terjual']
			jumlah_transaksi = form.cleaned_data['jumlah_transaksi']            
			produk_rusak = form.cleaned_data['produk_rusak']
			sisa_produk=form.cleaned_data['sisa_produk']
			stok_awal= form.cleaned_data['stok_awal']
			stok_akhir= form.cleaned_data['stok_akhir']
			hari_periode= form.cleaned_data['hari_periode']
			id_list= form.cleaned_data['id_list']


			entrydata = EntryData.objects.create(
				product=product, kuantitas_terjual=kuantitas_terjual, jumlah_transaksi=jumlah_transaksi, produk_rusak=produk_rusak, sisa_produk= sisa_produk ,stok_awal=stok_awal, stok_akhir=stok_akhir, id_list=id_list
            )

			form = AddEntryData()
			context['form'] = form
			return self.render_to_response(context=context)

		return self.render_to_response(context=context)

@login_required(login_url='account:login')
def addlist(request):
	submitted = False
	if request.method =="POST":
		form= AddListForm (request.POST)
		if form.is_valid():
			form.save()
			listname = form.cleaned_data.get('listname')
			return HttpResponseRedirect('/inventdata/list')
	else:
		form= AddListForm
		if 'submitted' in request.GET:
			submitted=True

	return render (request, 'inventdata/tambahlist.html', {'form':form, 'submitted': submitted })

@login_required(login_url='account:login')
def inventdatahome(request):
	context ={
		'judul' : 'Invent Data Home'
	}

	return render (request, 'inventdata/inventdatahome.html', context)

@login_required(login_url='account:login')
def editentry(request, pk, identry):

	listdata = ListData.objects.get(id=pk)
	entrydata = EntryData.objects.get(id=identry)


	form= AddEntryData(instance=entrydata)

	if request.method =="POST":
		form= AddEntryData (request.POST, instance=entrydata)
		if form.is_valid():
			form.save()
			return redirect ('inventdata:detail', pk)
		else:
			print ('FORM IS INVALID')
	
	else:

		form=AddEntryData(instance=entrydata)


	context = {
		'form' : form,
		'listdata': listdata,
		'entrydata' : entrydata
	}

	return render (request, "inventdata/editdata.html", context)

@login_required(login_url='account:login')
def deleteentry (request,pk, id):
	entrydata= EntryData.objects.get(id=id)
	entrydata.delete()
	return redirect ('inventdata:detail', pk)

@login_required(login_url='account:login')
def entryadd(request, pk):
	listdata = ListData.objects.get(id=pk)
	product = Product.objects.all()

	if request.method =="POST":
		form= AddEntryData (request.POST, instance=listdata)
		if form.is_valid():
			form.save()
			product = form.cleaned_data.get('product')
			kuantitas_terjual = form.cleaned_data.get('kuantitas_terjual')
			jumlah_transaksi = form.cleaned_data.get('jumlah_transaksi')            
			produk_rusak = form.cleaned_data.get('produk_rusak')
			sisa_produk=form.cleaned_data.get('sisa_produk')
			stok_awal= form.cleaned_data.get('stok_awal')
			stok_akhir= form.cleaned_data.get('stok_akhir')
			hari_periode= form.cleaned_data.get('hari_periode')
			ed, created= EntryData.objects.update_or_create(
				product=product, id_list=listdata, defaults={"kuantitas_terjual":kuantitas_terjual, "jumlah_transaksi":jumlah_transaksi, "produk_rusak":produk_rusak, "sisa_produk":sisa_produk, "stok_awal":stok_awal, "stok_akhir":stok_akhir, "hari_periode":hari_periode})
			ed.save()
			return redirect ('inventdata:detail', pk)
		else:
			print ('FORM IS INVALID')
			return redirect ('inventdata:add-entry', pk)

	
	else:
		form=AddEntryData()


	context = {
		'form' : form,
		'listdata' : listdata,
		'product' : product
	}

	return render (request, "inventdata/tambahdata2.html", context)

@login_required(login_url='account:login')
def uploadentry (request, pk):
	listdata = ListData.objects.get(id=pk)
	error_message=None
	success_message=None

	form = CsvForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		form= CsvForm()
		print("PASS 1")

		obj= CSV.objects.get(activated=False)
		print("PASS 2")
		dataobat = []
		print("PASS 3")
		with open (obj.file_name.path, 'r') as f:
			reader = csv.reader(f, delimiter=",")
			for row in reader:
				dataobat.append(row)

		labels = dataobat.pop(0)
		print (dataobat)

		for row in dataobat:
			product= row[0]
			kuantitas_terjual= int(row[1])
			jumlah_transaksi= int(row[2])
			produk_rusak= int(row[3])
			sisa_produk=int(row[4])
			stok_awal= int(row[5])
			stok_akhir= int(row[6])


			try:
				product_obj= Product.objects.get(name__iexact=product)
			except Product.DoesNotExist:
				product_obj=None



			if product_obj is not None:
				list_obj= ListData.objects.get(id=pk)
				entry_obj, created= EntryData.objects.update_or_create(
				product=product_obj, id_list=listdata, defaults={"kuantitas_terjual":kuantitas_terjual, "jumlah_transaksi":jumlah_transaksi, "produk_rusak":produk_rusak, "sisa_produk":sisa_produk, "stok_awal":stok_awal, "stok_akhir":stok_akhir})
				entry_obj.save()
		             

		obj.activated=True
		obj.save()
		messages.success(request, 'Berhasil Menambahkan Data')
        


	context = {
		'form': form,
		'listdata': listdata

	 }
	return render(request, 'inventdata/upload.html', context)

@login_required(login_url='account:login')
def uploadperiode (request, pk):
	listdata = ListData.objects.get(id=pk)
	error_message=None
	success_message=None

	form = CsvForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		form= CsvForm()
		print("PASS 1")

		obj= CSV.objects.get(activated=False)
		print("PASS 2")
		dataobat = []
		print("PASS 3")
		with open (obj.file_name.path, 'r') as f:
			reader = csv.reader(f, delimiter=",")
			for row in reader:
				dataobat.append(row)

		labels = dataobat.pop(0)
		print (dataobat)

		for row in dataobat:
			product= row[0]
			kuantitas_terjual= int(row[1])
			jumlah_transaksi= int(row[2])
			produk_rusak= int(row[3])
			sisa_produk=int(row[4])
			stok_awal= int(row[5])
			stok_akhir= int(row[6])
			hari_periode=int(row[7])
			

			try:
				product_obj= Product.objects.get(name__iexact=product)
			except Product.DoesNotExist:
				product_obj=None



			if product_obj is not None:
				list_obj= ListData.objects.get(id=pk)
				entry_obj, created= EntryData.objects.update_or_create(
				product=product_obj, id_list=listdata, defaults={"kuantitas_terjual":kuantitas_terjual, "jumlah_transaksi":jumlah_transaksi, "produk_rusak":produk_rusak, "sisa_produk":sisa_produk, "stok_awal":stok_awal, "stok_akhir":stok_akhir, "hari_periode":hari_periode})
				entry_obj.save()
		             

		obj.activated=True
		obj.save()
		messages.success(request, 'Berhasil Menambahkan Data')

        


	context = {
		'form': form,
		'listdata': listdata

	 }
	return render(request, 'inventdata/uploadperiode.html', context)

@login_required(login_url='account:login')
def tryanalysis(request, pk):
	if request.method == "POST":
		if request.POST.get('nilaik'):
			nilai_k=int(request.POST['nilaik'])
			entrydata = EntryData.objects.filter(id_list=pk)
			listdata = ListData.objects.get(id=pk)


			if len(entrydata)>0:
			#ed_df= pd.DataFrame(entrydata.values())
				ed_data=[]
				for ed in entrydata:
					obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
					}
					ed_data.append(obj)

				entrydata_df=pd.DataFrame(ed_data)
			#print(entrydata_df)

				column_names = [
			 	   'kuantitas_terjual',
			 	   'jumlah_transaksi',
			 	   'produk_rusak',
			 	   'tor',
			 	   'wsp'
				]
			#ambil kolom data yang dipilih sebagai parameter
				x_array = np.array(entrydata_df.loc[:, column_names])
			#print(x_array)
			#print("-------------")

			#normalisasi data
				x_scaledd = zscore(x_array, ddof=1)
				x_scaled=np.nan_to_num(x_scaledd)

			#print(x_scaled)
				norm_df=pd.DataFrame(x_scaled)
				json_records = norm_df.reset_index().to_json(orient ='records')
				arr4 = []
				arr4 = json.loads(json_records)
			#print(arr4)
			# Menentukan kluster dari data	
				KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
			#print("-------------")	
			#print(KM_5_clusters.cluster_centers_)# append labels to points

			# Menambahkan kolom "kluster" dalam data frame
				entrydata_df['cluster'] = KM_5_clusters.labels_
			#print("-------------")
			# print (entrydata_df['cluster'])
			# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
			# print("-------------")
			# print (product_df)
			#display ccenter
				c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
				json_records = c.reset_index().to_json(orient ='records')
				arr3 = []
				arr3 = json.loads(json_records)

				ccloc=KM_5_clusters.medoid_indices_
			#display_data dan hasil cluster
				json_records = entrydata_df.reset_index().to_json(orient ='records')
				arr = []
				arr = json.loads(json_records)
			#print("-------------")
			# print(arr)
		    #silhouette score average for all of the cluster
				labels= entrydata_df['cluster']
				s_avg= metrics.silhouette_score(x_scaled, labels)
			#print("-------------")
			#print('Silhouette Score:', s_avg)

		    #silhouette score average for each clusters
		    #silhouette score for each data (idk if i can do this )
		    #graph
				a=entrydata_df.loc[:, column_names]
				bb=zscore(a, ddof=1)
				cb=np.nan_to_num(bb)
				b=pd.DataFrame(cb)
				json_records = a.reset_index().to_json(orient ='records')
				ar2 = []
				ar2 = json.loads(json_records) 



				chart= try_get_plot(request,b,pk)

			else:
				b=[]
				chart=try_get_plot(request, b,pk)
				arr= []
				s_avg= "TIDAK ADA NILAI SCORE"
				arr3= []
				ar2= []
				arr4= []
				ccloc= []
		else:
			nilai_k=5
			entrydata = EntryData.objects.filter(id_list=pk)
			listdata = ListData.objects.get(id=pk)


			if len(entrydata)>0:
			#ed_df= pd.DataFrame(entrydata.values())
				ed_data=[]
				for ed in entrydata:
					obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
					}
					ed_data.append(obj)

				entrydata_df=pd.DataFrame(ed_data)
			#print(entrydata_df)

				column_names = [
			 	   'kuantitas_terjual',
			 	   'jumlah_transaksi',
			 	   'produk_rusak',
			 	   'tor',
			 	   'wsp'
				]
			#ambil kolom data yang dipilih sebagai parameter
				x_array = np.array(entrydata_df.loc[:, column_names])
			#print(x_array)
			#print("-------------")

			#normalisasi data
				x_scaledd = zscore(x_array, ddof=1)
				x_scaled=np.nan_to_num(x_scaledd)
			#print(x_scaled)
				norm_df=pd.DataFrame(x_scaled)
				json_records = norm_df.reset_index().to_json(orient ='records')
				arr4 = []
				arr4 = json.loads(json_records)
			#print(arr4)
			# Menentukan kluster dari data	
				KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
			#print("-------------")	
			#print(KM_5_clusters.cluster_centers_)# append labels to points

			# Menambahkan kolom "kluster" dalam data frame
				entrydata_df['cluster'] = KM_5_clusters.labels_
			#print("-------------")
			# print (entrydata_df['cluster'])
			# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
			# print("-------------")
			# print (product_df)
			#display ccenter
				c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
				json_records = c.reset_index().to_json(orient ='records')
				arr3 = []
				arr3 = json.loads(json_records)

				ccloc=KM_5_clusters.medoid_indices_
		




			#display_data dan hasil cluster
				json_records = entrydata_df.reset_index().to_json(orient ='records')
				arr = []
				arr = json.loads(json_records)
			#print("-------------")
			# print(arr)
		    #silhouette score average for all of the cluster
				labels= entrydata_df['cluster']
				s_avg= metrics.silhouette_score(x_scaled, labels)
			#print("-------------")
			#print('Silhouette Score:', s_avg)

		    #silhouette score average for each clusters
		    #silhouette score for each data (idk if i can do this )
		    #graph
				a=entrydata_df.loc[:, column_names]
				bb=zscore(a, ddof=1)
				cb=np.nan_to_num(bb)
				b=pd.DataFrame(cb)
				json_records = a.reset_index().to_json(orient ='records')
				ar2 = []
				ar2 = json.loads(json_records) 



				chart= get_plot(b,pk)

			else:
				b=[]
				chart=get_plot(b,pk)
				arr= []
				s_avg= "TIDAK ADA NILAI SCORE"
				arr3= []
				ar2= []
				arr4= []
				ccloc= []

		context = {
				'chart':chart,
				'entrydata':entrydata,
		        'hasilcluster': arr,
		        'silhouette': s_avg,
		        'clustercenter': arr3,
		        'dataawal': ar2,
		        'datanormalisasi': arr4,
		        'posisimedoid':ccloc,
		        'listdata': listdata,
		        'nilaik': nilai_k,


    	}
	return render(request, 'inventdata/tryanalysis.html', context)

@login_required(login_url='account:login')
def tryanalysis2(request, pk):
	if request.method == "POST":
		if request.POST.get('nilaik'):
			nilai_k=int(request.POST['nilaik'])
			entrydata = EntryData.objects.filter(id_list=pk)
			listdata = ListData.objects.get(id=pk)


			if len(entrydata)>0:
			#ed_df= pd.DataFrame(entrydata.values())
				ed_data=[]
				for ed in entrydata:
					obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'sisa_produk': ed.sisa_produk,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
					}
					ed_data.append(obj)

				entrydata_df=pd.DataFrame(ed_data)
			#print(entrydata_df)

				column_names = [
			 	   'kuantitas_terjual',
			 	   'jumlah_transaksi',
			 	   'sisa_produk',
			 	   'produk_rusak',
				]
			#ambil kolom data yang dipilih sebagai parameter
				x_array = np.array(entrydata_df.loc[:, column_names])
			#print(x_array)
			#print("-------------")

			#normalisasi data
				x_scaledd = zscore(x_array, ddof=1)
				x_scaled=np.nan_to_num(x_scaledd)

			#print(x_scaled)
				norm_df=pd.DataFrame(x_scaled)
				json_records = norm_df.reset_index().to_json(orient ='records')
				arr4 = []
				arr4 = json.loads(json_records)
			#print(arr4)
			# Menentukan kluster dari data	
				KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
			#print("-------------")	
			#print(KM_5_clusters.cluster_centers_)# append labels to points

			# Menambahkan kolom "kluster" dalam data frame
				entrydata_df['cluster'] = KM_5_clusters.labels_
			#print("-------------")
			# print (entrydata_df['cluster'])
			# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
			# print("-------------")
			# print (product_df)
			#display ccenter
				c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
				json_records = c.reset_index().to_json(orient ='records')
				arr3 = []
				arr3 = json.loads(json_records)

				ccloc=KM_5_clusters.medoid_indices_
			#display_data dan hasil cluster
				json_records = entrydata_df.reset_index().to_json(orient ='records')
				arr = []
				arr = json.loads(json_records)
			#print("-------------")
			# print(arr)
		    #silhouette score average for all of the cluster
				labels= entrydata_df['cluster']
				s_avg= metrics.silhouette_score(x_scaled, labels)
			#print("-------------")
			#print('Silhouette Score:', s_avg)

		    #silhouette score average for each clusters
		    #silhouette score for each data (idk if i can do this )
		    #graph
				a=entrydata_df.loc[:, column_names]
				bb=zscore(a, ddof=1)
				cb=np.nan_to_num(bb)
				b=pd.DataFrame(cb)
				json_records = a.reset_index().to_json(orient ='records')
				ar2 = []
				ar2 = json.loads(json_records) 



				chart= try_get_plot2(request,b,pk)

			else:
				b=[]
				chart=try_get_plot2(request, b,pk)
				arr= []
				s_avg= "TIDAK ADA NILAI SCORE"
				arr3= []
				ar2= []
				arr4= []
				ccloc= []
		else:
			nilai_k=5
			entrydata = EntryData.objects.filter(id_list=pk)
			listdata = ListData.objects.get(id=pk)


			if len(entrydata)>0:
			#ed_df= pd.DataFrame(entrydata.values())
				ed_data=[]
				for ed in entrydata:
					obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'sisa_produk': ed.sisa_produk,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
					}
					ed_data.append(obj)

				entrydata_df=pd.DataFrame(ed_data)
			#print(entrydata_df)

				column_names = [
			 	   'kuantitas_terjual',
			 	   'jumlah_transaksi',
			 	   'sisa_produk',			 	   
			 	   'produk_rusak',


				]
			#ambil kolom data yang dipilih sebagai parameter
				x_array = np.array(entrydata_df.loc[:, column_names])
			#print(x_array)
			#print("-------------")

			#normalisasi data
				x_scaledd = zscore(x_array, ddof=1)
				x_scaled=np.nan_to_num(x_scaledd)
			#print(x_scaled)
				norm_df=pd.DataFrame(x_scaled)
				json_records = norm_df.reset_index().to_json(orient ='records')
				arr4 = []
				arr4 = json.loads(json_records)
			#print(arr4)
			# Menentukan kluster dari data	
				KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
			#print("-------------")	
			#print(KM_5_clusters.cluster_centers_)# append labels to points

			# Menambahkan kolom "kluster" dalam data frame
				entrydata_df['cluster'] = KM_5_clusters.labels_
			#print("-------------")
			# print (entrydata_df['cluster'])
			# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
			# print("-------------")
			# print (product_df)
			#display ccenter
				c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
				json_records = c.reset_index().to_json(orient ='records')
				arr3 = []
				arr3 = json.loads(json_records)

				ccloc=KM_5_clusters.medoid_indices_
		




			#display_data dan hasil cluster
				json_records = entrydata_df.reset_index().to_json(orient ='records')
				arr = []
				arr = json.loads(json_records)
			#print("-------------")
			# print(arr)
		    #silhouette score average for all of the cluster
				labels= entrydata_df['cluster']
				s_avg= metrics.silhouette_score(x_scaled, labels)
			#print("-------------")
			#print('Silhouette Score:', s_avg)

		    #silhouette score average for each clusters
		    #silhouette score for each data (idk if i can do this )
		    #graph
				a=entrydata_df.loc[:, column_names]
				bb=zscore(a, ddof=1)
				cb=np.nan_to_num(bb)
				b=pd.DataFrame(cb)
				json_records = a.reset_index().to_json(orient ='records')
				ar2 = []
				ar2 = json.loads(json_records) 



				chart= get_plot(b,pk)

			else:
				b=[]
				chart=get_plot(b,pk)
				arr= []
				s_avg= "TIDAK ADA NILAI SCORE"
				arr3= []
				ar2= []
				arr4= []
				ccloc= []

		context = {
				'chart':chart,
				'entrydata':entrydata,
		        'hasilcluster': arr,
		        'silhouette': s_avg,
		        'clustercenter': arr3,
		        'dataawal': ar2,
		        'datanormalisasi': arr4,
		        'posisimedoid':ccloc,
		        'listdata': listdata,
		        'nilaik': nilai_k,


    	}
	return render(request, 'inventdata/tryanalysis2.html', context)

@login_required(login_url='account:login')
def tryanalysis3(request, pk):
	if request.method == "POST":
		if request.POST.get('nilaik'):
			nilai_k=int(request.POST['nilaik'])
			entrydata = EntryData.objects.filter(id_list=pk)
			listdata = ListData.objects.get(id=pk)


			if len(entrydata)>0:
			#ed_df= pd.DataFrame(entrydata.values())
				ed_data=[]
				for ed in entrydata:
					obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
					}
					ed_data.append(obj)

				entrydata_df=pd.DataFrame(ed_data)
			#print(entrydata_df)

				column_names = [
			 	   'produk_rusak',
			 	   'tor',
			 	   'wsp'
				]
			#ambil kolom data yang dipilih sebagai parameter
				x_array = np.array(entrydata_df.loc[:, column_names])
			#print(x_array)
			#print("-------------")

			#normalisasi data
				x_scaledd = zscore(x_array, ddof=1)
				x_scaled=np.nan_to_num(x_scaledd)

			#print(x_scaled)
				norm_df=pd.DataFrame(x_scaled)
				json_records = norm_df.reset_index().to_json(orient ='records')
				arr4 = []
				arr4 = json.loads(json_records)
			#print(arr4)
			# Menentukan kluster dari data	
				KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
			#print("-------------")	
			#print(KM_5_clusters.cluster_centers_)# append labels to points

			# Menambahkan kolom "kluster" dalam data frame
				entrydata_df['cluster'] = KM_5_clusters.labels_
			#print("-------------")
			# print (entrydata_df['cluster'])
			# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
			# print("-------------")
			# print (product_df)
			#display ccenter
				c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
				json_records = c.reset_index().to_json(orient ='records')
				arr3 = []
				arr3 = json.loads(json_records)

				ccloc=KM_5_clusters.medoid_indices_
			#display_data dan hasil cluster
				json_records = entrydata_df.reset_index().to_json(orient ='records')
				arr = []
				arr = json.loads(json_records)
				# print("-------arr------")
				# print(arr)
		
		    #silhouette score average for all of the cluster
				labels= entrydata_df['cluster']
				s_avg= metrics.silhouette_score(x_scaled, labels)
				meanniee= entrydata_df.groupby(['cluster']).agg("mean")
				meannie=pd.DataFrame(meanniee).iloc[:, 6:9]
				jf = meannie.reset_index().to_json(orient ='records')
				mf = []
				mf = json.loads(jf)
				# print("meannie")
				# print(meannie)
				# print(mf)
				df_new0 = entrydata_df.loc[entrydata_df['cluster'] == 0]
				mean0=df_new0.iloc[:, 7:11] .mean()
				j0 = mean0.reset_index().to_json(orient ='records')
				m0 = []
				m0 = json.loads(j0)
				df_new1 = entrydata_df.loc[entrydata_df['cluster'] == 1]
				mean1=df_new1.iloc[:, 7:11] .mean()
				j1 = mean1.reset_index().to_json(orient ='records')
				m1 = []
				m1 = json.loads(j1)
				df_new2 = entrydata_df.loc[entrydata_df['cluster'] == 2]
				mean2=df_new2.iloc[:, 7:11] .mean()
				j2 = mean2.reset_index().to_json(orient ='records')
				m2 = []
				m2 = json.loads(j2)
				df_new3 = entrydata_df.loc[entrydata_df['cluster'] == 3]
				mean3=df_new3.iloc[:, 7:11] .mean()
				j3 = mean3.reset_index().to_json(orient ='records')
				m3 = []
				m3 = json.loads(j3)
				df_new4 = entrydata_df.loc[entrydata_df['cluster'] == 4]
				mean4=df_new4.iloc[:, 7:11] .mean()
				j4 = mean4.reset_index().to_json(orient ='records')
				m4 = []
				m4 = json.loads(j4)
				#mean0=df_new2.mean()
				# print("-------mean0------")
				# print(mean0)
				# print("-------mean1------")
				# print(mean1)	
				# print("-------mean2------")
				# print(mean2)	
				# print("-------mean3------")
				# print(mean3)	
				# print("-------mean4------")
				# print(mean4)			
			#print("-------------")
			#print('Silhouette Score:', s_avg)

		    #silhouette score average for each clusters
		    #silhouette score for each data (idk if i can do this )
		    #graph
				a=entrydata_df.loc[:, column_names]
				bb=zscore(a, ddof=1)
				cb=np.nan_to_num(bb)
				b=pd.DataFrame(cb)
				json_records = a.reset_index().to_json(orient ='records')
				ar2 = []
				ar2 = json.loads(json_records) 



				chart= try_get_plot3(request,b,pk)

			else:
				b=[]
				chart=try_get_plot3(request, b,pk)
				arr= []
				s_avg= "TIDAK ADA NILAI SCORE"
				arr3= []
				ar2= []
				arr4= []
				ccloc= []
				mf=[]
				m0=[]
				m1=[]
				m2=[]
				m3=[]
				m4=[]
		else:
			nilai_k=5
			entrydata = EntryData.objects.filter(id_list=pk)
			listdata = ListData.objects.get(id=pk)


			if len(entrydata)>0:
			#ed_df= pd.DataFrame(entrydata.values())
				ed_data=[]
				for ed in entrydata:
					obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
					}
					ed_data.append(obj)

				entrydata_df=pd.DataFrame(ed_data)
			#print(entrydata_df)

				column_names = [
			 	   'produk_rusak',
			 	   'tor',
			 	   'wsp'

				]
			#ambil kolom data yang dipilih sebagai parameter
				x_array = np.array(entrydata_df.loc[:, column_names])
			#print(x_array)
			#print("-------------")

			#normalisasi data
				x_scaledd = zscore(x_array, ddof=1)
				x_scaled=np.nan_to_num(x_scaledd)
			#print(x_scaled)
				norm_df=pd.DataFrame(x_scaled)
				json_records = norm_df.reset_index().to_json(orient ='records')
				arr4 = []
				arr4 = json.loads(json_records)
			#print(arr4)
			# Menentukan kluster dari data	
				KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
			#print("-------------")	
			#print(KM_5_clusters.cluster_centers_)# append labels to points

			# Menambahkan kolom "kluster" dalam data frame
				entrydata_df['cluster'] = KM_5_clusters.labels_
			#print("-------------")
			# print (entrydata_df['cluster'])
			# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
			# print("-------------")
			# print (product_df)
			#display ccenter
				c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
				json_records = c.reset_index().to_json(orient ='records')
				arr3 = []
				arr3 = json.loads(json_records)

				ccloc=KM_5_clusters.medoid_indices_
		




			#display_data dan hasil cluster
				json_records = entrydata_df.reset_index().to_json(orient ='records')
				arr = []
				arr = json.loads(json_records)
			#print("-------------")
			# print(arr)
		    #silhouette score average for all of the cluster
				labels= entrydata_df['cluster']
				meanniee= entrydata_df.groupby(['cluster']).agg({'mean'})
				meannie=pd.DataFrame(meanniee).iloc[:, 6:9]
				jf = meannie.reset_index().to_json(orient ='records')
				mf = []
				mf = json.loads(jf)
				df_new0 = entrydata_df.loc[entrydata_df['cluster'] == 0]
				mean0=df_new0.iloc[:, 7:11] .mean()
				j0 = mean0.reset_index().to_json(orient ='records')
				m0 = []
				m0 = json.loads(j0)
				df_new1 = entrydata_df.loc[entrydata_df['cluster'] == 1]
				mean1=df_new1.iloc[:, 7:11] .mean()
				j1 = mean1.reset_index().to_json(orient ='records')
				m1 = []
				m1 = json.loads(j1)
				df_new2 = entrydata_df.loc[entrydata_df['cluster'] == 2]
				mean2=df_new2.iloc[:, 7:11] .mean()
				j2 = mean2.reset_index().to_json(orient ='records')
				m2 = []
				m2 = json.loads(j2)
				df_new3 = entrydata_df.loc[entrydata_df['cluster'] == 3]
				mean3=df_new3.iloc[:, 7:11] .mean()
				j3 = mean3.reset_index().to_json(orient ='records')
				m3 = []
				m3 = json.loads(j3)
				df_new4 = entrydata_df.loc[entrydata_df['cluster'] == 4]
				mean4=df_new4.iloc[:, 7:11] .mean()
				j4 = mean4.reset_index().to_json(orient ='records')
				m4 = []
				m4 = json.loads(j4)


				s_avg= metrics.silhouette_score(x_scaled, labels)
			#print("-------------")
			#print('Silhouette Score:', s_avg)

		    #silhouette score average for each clusters
		    #silhouette score for each data (idk if i can do this )
		    #graph
				a=entrydata_df.loc[:, column_names]
				bb=zscore(a, ddof=1)
				cb=np.nan_to_num(bb)
				b=pd.DataFrame(cb)
				json_records = a.reset_index().to_json(orient ='records')
				ar2 = []
				ar2 = json.loads(json_records) 



				chart= get_plot(b,pk)

			else:
				b=[]
				chart=get_plot(b,pk)
				arr= []
				s_avg= "TIDAK ADA NILAI SCORE"
				arr3= []
				ar2= []
				arr4= []
				ccloc= []
				mf=[]
				m0=[]
				m1=[]
				m2=[]
				m3=[]
				m4=[]


		context = {
				'chart':chart,
				'entrydata':entrydata,
		        'hasilcluster': arr,
		        'silhouette': s_avg,
		        'clustercenter': arr3,
		        'dataawal': ar2,
		        'datanormalisasi': arr4,
		        'posisimedoid':ccloc,
		        'listdata': listdata,
		        'nilaik': nilai_k,
		        'm0': m0,
		        'm1': m1,
		        'm2': m2,
		        'm3': m3,
		        'm4': m4,
		        'mf': mf, 


    	}
	return render(request, 'inventdata/tryanalysis3.html', context)

@login_required(login_url='account:login')
def analysis(request,pk):

	nilai_k = 5
	#conver into dataframe
	entrydata = EntryData.objects.filter(id_list=pk)
	listdata = ListData.objects.get(id=pk)


	if len(entrydata)>0:
		#ed_df= pd.DataFrame(entrydata.values())
		ed_data=[]
		for ed in entrydata:
			obj={
			'product': ed.product.name,
			'product_id': ed.product_id,
			'kuantitas_terjual': ed.kuantitas_terjual,
			'jumlah_transaksi': ed.jumlah_transaksi,
			'hari_periode':ed.hari_periode,
			'stok_awal': ed.stok_awal,
			'stok_akhir': ed.stok_akhir,
			'produk_rusak': ed.produk_rusak,
			'tor': ed.tor,
			'wsp': ed.wsp,
			}
			ed_data.append(obj)

		entrydata_df=pd.DataFrame(ed_data)
		#print(entrydata_df)

		column_names = [
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, column_names])
		#print(x_array)
		#print("-------------")

		#normalisasi data
		x_scaled = zscore(x_array, ddof=1)
		#print(x_scaled)
		norm_df=pd.DataFrame(x_scaled)
		json_records = norm_df.reset_index().to_json(orient ='records')
		arr4 = []
		arr4 = json.loads(json_records)
		#print(arr4)
		# Menentukan kluster dari data	
		KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
		#print("-------------")	
		#print(KM_5_clusters.cluster_centers_)# append labels to points

		# Menambahkan kolom "kluster" dalam data frame
		entrydata_df['cluster'] = KM_5_clusters.labels_
		#print("-------------")
		# print (entrydata_df['cluster'])
		# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
		# print("-------------")
		# print (product_df)
		#display ccenter
		c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
		json_records = c.reset_index().to_json(orient ='records')
		arr3 = []
		arr3 = json.loads(json_records)

		ccloc=KM_5_clusters.medoid_indices_
	




		#display_data dan hasil cluster
		json_records = entrydata_df.reset_index().to_json(orient ='records')
		arr = []
		arr = json.loads(json_records)
		#print("-------------")
		# print(arr)
	    #silhouette score average for all of the cluster
		labels= entrydata_df['cluster']
		s_avg= metrics.silhouette_score(x_scaled, labels)
		#print("-------------")
		#print('Silhouette Score:', s_avg)

	    #silhouette score average for each clusters
	    #silhouette score for each data (idk if i can do this )
	    #graph
		a=entrydata_df.loc[:, column_names]
		b=zscore(a, ddof=1)
		json_records = a.reset_index().to_json(orient ='records')
		ar2 = []
		ar2 = json.loads(json_records) 



		chart= get_plot(b,pk)

	else:
		b=[]
		chart=get_plot(b,pk)
		arr= []
		s_avg= "TIDAK ADA NILAI SCORE"
		arr3= []
		ar2= []
		arr4= []
		ccloc= []


	context = {
		'chart':chart,
		'entrydata':entrydata,
        'hasilcluster': arr,
        'silhouette': s_avg,
        'clustercenter': arr3,
        'dataawal': ar2,
        'datanormalisasi': arr4,
        'posisimedoid':ccloc,
        'listdata': listdata





    }

	return render(request, 'inventdata/analysis.html', context)



@login_required(login_url='account:login')
def try_analysis_pdf(request, pk):

	#CREATE BYTSTREAM BUFFER
	# buf=io.BytesIO()
	# #create canvas 
	# c= canvas.Canvas (buf,pagesize=letter, bottomup=0)
	# #text objek di canvas
	# textob=c.beginText()
	# textob.setTextOrigin(inch,inch)
	# textob.setFont("Helvetica", 14)

	#logic data analysis
	nilai_k = int(request.POST.get('nilai_k_select',5))
	#conver into dataframe
	listdata = ListData.objects.get(id=pk)
	entrydata = EntryData.objects.filter(id_list=pk)


	if len(entrydata)>0:
		#ed_df= pd.DataFrame(entrydata.values())
		ed_data=[]
		for ed in entrydata:
			obj={
			'product': ed.product.name,
			'product_id': ed.product_id,
			'kuantitas_terjual': ed.kuantitas_terjual,
			'jumlah_transaksi': ed.jumlah_transaksi,
			'hari_periode':ed.hari_periode,
			'stok_awal': ed.stok_awal,
			'stok_akhir': ed.stok_akhir,
			'produk_rusak': ed.produk_rusak,
			'tor': ed.tor,
			'wsp': ed.wsp,
			}
			ed_data.append(obj)

		entrydata_df=pd.DataFrame(ed_data)
		#print(entrydata_df)

		column_names = [
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, column_names])
		#print(x_array)
		#print("-------------")

		#normalisasi data
		x_scaledd = zscore(x_array, ddof=1)
		x_scaled=np.nan_to_num(x_scaledd)
		#print(x_scaled)
		norm_df=pd.DataFrame(x_scaled)
		json_records = norm_df.reset_index().to_json(orient ='records')
		arr4 = []
		arr4 = json.loads(json_records)
		#print(arr4)
		# Menentukan kluster dari data	
		KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
		#print("-------------")	
		#print(KM_5_clusters.cluster_centers_)# append labels to points

		# Menambahkan kolom "kluster" dalam data frame
		entrydata_df['cluster'] = KM_5_clusters.labels_
		#print("-------------")
		# print (entrydata_df['cluster'])
		# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
		# print("-------------")
		# print (product_df)
		#display ccenter
		c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
		json_records = c.reset_index().to_json(orient ='records')
		arr3 = []
		arr3 = json.loads(json_records)

		ccloc=KM_5_clusters.medoid_indices_

		#display_data dan hasil cluster
		cns = [
		   'product',
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp',
	 	   'cluster'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, cns])
		json_records = entrydata_df.reset_index().to_json(orient ='records')
		arr = []
		arr = json.loads(json_records)
		#print("-------------")
		# print(arr)
	    #silhouette score average for all of the cluster
		labels= entrydata_df['cluster']
		s_avg= metrics.silhouette_score(x_scaled, labels)
		#print("-------------")
		#print('Silhouette Score:', s_avg)

	    #silhouette score average for each clusters
	    #silhouette score for each data (idk if i can do this )
	    #graph
		#chart= get_plot(norm_df,pk)
		a=entrydata_df.loc[:, column_names]
		bb=zscore(a, ddof=1)
		cb=np.nan_to_num(bb)
		b=pd.DataFrame(cb)
		json_records = a.reset_index().to_json(orient ='records')
		ar2 = []
		ar2 = json.loads(json_records) 




		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		namalist  = "Nama List Data: "+ listdata.nama_list
		nilaikterpilih = "Nilai k: "+ request.POST.get('nilai_k_select',"5")
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]

		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def body(txt, style=ParaStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para, s]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = p(nilaikterpilih)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(namalist, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		myabstract = p(Abstract)
		t1d=body(T1Desc)
		t2d=body(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dfn=entrydata_df.loc[:, cns].sort_values('cluster').rename(columns = {'product':'Produk', 'kuantitas_terjual': 'Kuantitas Terjual', 'jumlah_transaksi': 'Jumlah Transaksi', 'produk_rusak': 'Produk Rusak', 'tor': 'TOR', 'wsp': 'WSP', 'cluster': 'Cluster'}) 
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		xar = np.array(entrydata_df.loc[:, column_names])
		axsc = zscore(xar, ddof=1)
		xsc=np.nan_to_num(axsc)
		# rpdt=np.array(dfn).tolist()
		t1 = Table(rpdt, colWidths=[82,82],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		c2=dfn.loc[KM_5_clusters.medoid_indices_]
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		labels= entrydata_df['cluster']
		sscore=float(metrics.silhouette_score(xsc, labels))
		teksket="Silhouette Score :"
		ket= p(teksket)
		t3_info= [ket]
		score=pd.DataFrame(columns = ['Silhouette Score'])
		s_score=score.append({'Silhouette Score': sscore}, ignore_index = True)
		rpdt3=s_score.values.tolist()
		t3 = Table(rpdt3, colWidths=[20,20], hAlign='LEFT');
		print(rpdt3)
		chart_info=[ctitle]
		buffer = io.BytesIO()

		filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list + str(listdata.id)+request.user.username+".png")

		def get_python_image():

			if not os.path.exists(filename) :
				response = print("no picture")
				f = open(filename, 'w')
				f.write(response.read())
				f.close()

		get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter, rightMargin=15, leftMargin=15)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.append(PageBreak())
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
		element.extend(t3_info)
		element.append(t3)
		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"



	else:



		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		URL = "Nama List Data: "+ listdata.nama_list
		email = "Tidak ada data"
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]


		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = header(URL, sep=0.1, style=ParaStyle)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(email, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		t3= p("Tidak Ada Data. Tidak Ada Visualisasi Silhouette Score")
		myabstract = p(Abstract)
		t1d=p(T1Desc)
		t2d=p(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		chart_info=[ctitle, t3]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dc=pd.DataFrame(columns = ['Produk','Kuantitas Terjual', 'Jumlah Transaksi', 'Produk Rusak',  'TOR',  'WSP',  'Cluster']) 
		dfn = dc.append({'Produk': 'Tidak ada Data','Kuantitas Terjual' : 'Tidak ada Data', 'Jumlah Transaksi' : 'Tidak ada Data', 'Produk Rusak' : 'Tidak ada Data',  'TOR' : 'Tidak ada Data',  'WSP' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		t1 = Table(rpdt, colWidths=[75,75],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		dc2=pd.DataFrame(columns = ['Produk','Kuantitas Terjual', 'Jumlah Transaksi', 'Produk Rusak',  'TOR',  'WSP',  'Cluster']) 
		c2= dc2.append({'Produk': 'Tidak ada Data','Kuantitas Terjual' : 'Tidak ada Data', 'Jumlah Transaksi' : 'Tidak ada Data', 'Produk Rusak' : 'Tidak ada Data',  'TOR' : 'Tidak ada Data',  'WSP' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		buffer = io.BytesIO()


		# outfilename = listdata.nama_list+".pdf"
		# outfiledir = 'webprojectsnew/lenkoproject/media/reports'
		# outfilepath = os.path.join( outfiledir, outfilename )


		# # imgdata = cStringIO.StringIO()
		# # fig.savefig(imgdata, format='png')
		# # imgdata.seek(0)  # rewind the data

		# Image = ImageReader(fig)
		# filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list+".png")

		# def get_python_image():

		# 	if not os.path.exists(filename) :
		# 		response = print("no picture")
		# 		f = open(filename, 'w')
		# 		f.write(response.read())
		# 		f.close()

		# get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
#		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"

	return response



@login_required(login_url='account:login')
def try_analysis2_pdf(request, pk):

	#CREATE BYTSTREAM BUFFER
	# buf=io.BytesIO()
	# #create canvas 
	# c= canvas.Canvas (buf,pagesize=letter, bottomup=0)
	# #text objek di canvas
	# textob=c.beginText()
	# textob.setTextOrigin(inch,inch)
	# textob.setFont("Helvetica", 14)

	#logic data analysis
	nilai_k = int(request.POST.get('nilai_k_select',5))
	#conver into dataframe
	listdata = ListData.objects.get(id=pk)
	entrydata = EntryData.objects.filter(id_list=pk)


	if len(entrydata)>0:
		#ed_df= pd.DataFrame(entrydata.values())
		ed_data=[]
		for ed in entrydata:
			obj={
					'product': ed.product.name,
					'product_id': ed.product_id,
					'kuantitas_terjual': ed.kuantitas_terjual,
					'jumlah_transaksi': ed.jumlah_transaksi,
					'hari_periode':ed.hari_periode,
					'sisa_produk': ed.sisa_produk,
					'stok_awal': ed.stok_awal,
					'stok_akhir': ed.stok_akhir,
					'produk_rusak': ed.produk_rusak,
					'tor': ed.tor,
					'wsp': ed.wsp,
			}
			ed_data.append(obj)

		entrydata_df=pd.DataFrame(ed_data)
		#print(entrydata_df)

		column_names = [
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'sisa_produk',
	 	   'produk_rusak'


		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, column_names])
		#print(x_array)
		#print("-------------")

		#normalisasi data
		x_scaledd = zscore(x_array, ddof=1)
		x_scaled=np.nan_to_num(x_scaledd)
		#print(x_scaled)
		norm_df=pd.DataFrame(x_scaled)
		json_records = norm_df.reset_index().to_json(orient ='records')
		arr4 = []
		arr4 = json.loads(json_records)
		#print(arr4)
		# Menentukan kluster dari data	
		KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
		#print("-------------")	
		#print(KM_5_clusters.cluster_centers_)# append labels to points

		# Menambahkan kolom "kluster" dalam data frame
		entrydata_df['cluster'] = KM_5_clusters.labels_
		#print("-------------")
		# print (entrydata_df['cluster'])
		# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
		# print("-------------")
		# print (product_df)
		#display ccenter
		c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
		json_records = c.reset_index().to_json(orient ='records')
		arr3 = []
		arr3 = json.loads(json_records)

		ccloc=KM_5_clusters.medoid_indices_

		#display_data dan hasil cluster
		cns = [
		   'product',
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'sisa_produk',
	 	   'produk_rusak',
	 	   'cluster'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, cns])
		json_records = entrydata_df.reset_index().to_json(orient ='records')
		arr = []
		arr = json.loads(json_records)
		#print("-------------")
		# print(arr)
	    #silhouette score average for all of the cluster
		labels= entrydata_df['cluster']
		s_avg= metrics.silhouette_score(x_scaled, labels)
		#print("-------------")
		#print('Silhouette Score:', s_avg)

	    #silhouette score average for each clusters
	    #silhouette score for each data (idk if i can do this )
	    #graph
		#chart= get_plot(norm_df,pk)
		a=entrydata_df.loc[:, column_names]
		bb=zscore(a, ddof=1)
		cb=np.nan_to_num(bb)
		b=pd.DataFrame(cb)
		json_records = a.reset_index().to_json(orient ='records')
		ar2 = []
		ar2 = json.loads(json_records) 




		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		namalist  = "Nama List Data: "+ listdata.nama_list
		nilaikterpilih = "Nilai k: "+ request.POST.get('nilai_k_select',"5")
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]

		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def body(txt, style=ParaStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para, s]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = p(nilaikterpilih)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(namalist, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		myabstract = p(Abstract)
		t1d=body(T1Desc)
		t2d=body(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dfn=entrydata_df.loc[:, cns].sort_values('cluster').rename(columns = {'product':'Produk', 'kuantitas_terjual': 'Kuantitas Terjual', 'jumlah_transaksi': 'Jumlah Transaksi','sisa_produk': 'Sisa Produk', 'produk_rusak': 'Produk Rusak', 'cluster': 'Cluster'}) 
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		xar = np.array(entrydata_df.loc[:, column_names])
		axsc = zscore(xar, ddof=1)
		xsc=np.nan_to_num(axsc)
		# rpdt=np.array(dfn).tolist()
		t1 = Table(rpdt, colWidths=[82,82],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		c2=dfn.loc[KM_5_clusters.medoid_indices_]
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		labels= entrydata_df['cluster']
		sscore=float(metrics.silhouette_score(xsc, labels))
		teksket="Silhouette Score :"
		ket= p(teksket)
		t3_info= [ket]
		score=pd.DataFrame(columns = ['Silhouette Score'])
		s_score=score.append({'Silhouette Score': sscore}, ignore_index = True)
		rpdt3=s_score.values.tolist()
		t3 = Table(rpdt3, colWidths=[20,20], hAlign='LEFT');
		print(rpdt3)
		chart_info=[ctitle]
		buffer = io.BytesIO()

		filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list + str(listdata.id)+request.user.username+"analisis 2"+".png")

		def get_python_image():

			if not os.path.exists(filename) :
				response = print("no picture")
				f = open(filename, 'w')
				f.write(response.read())
				f.close()

		get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter, rightMargin=15, leftMargin=15)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.append(PageBreak())
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
		element.extend(t3_info)
		element.append(t3)
		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report2.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report2.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"



	else:



		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		URL = "Nama List Data: "+ listdata.nama_list
		email = "Tidak ada data"
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]


		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = header(URL, sep=0.1, style=ParaStyle)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(email, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		t3= p("Tidak Ada Data. Tidak Ada Visualisasi Silhouette Score")
		myabstract = p(Abstract)
		t1d=p(T1Desc)
		t2d=p(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		chart_info=[ctitle, t3]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dc=pd.DataFrame(columns = ['Produk','Kuantitas Terjual', 'Jumlah Transaksi','Sisa Produk', 'Produk Rusak',  'Cluster']) 
		dfn = dc.append({'Produk': 'Tidak ada Data','Kuantitas Terjual' : 'Tidak ada Data', 'Jumlah Transaksi' : 'Tidak ada Data', 'Sisa Produk' : 'Tidak ada Data' ,'Produk Rusak' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		t1 = Table(rpdt, colWidths=[75,75],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		dc2=pd.DataFrame(columns = ['Produk','Kuantitas Terjual', 'Jumlah Transaksi', 'Sisa Produk' ,'Produk Rusak',  'Cluster']) 
		c2= dc2.append({'Produk': 'Tidak ada Data','Kuantitas Terjual' : 'Tidak ada Data', 'Jumlah Transaksi' : 'Tidak ada Data', 'Sisa Produk' : 'Tidak ada Data' ,'Produk Rusak' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		buffer = io.BytesIO()


		# outfilename = listdata.nama_list+".pdf"
		# outfiledir = 'webprojectsnew/lenkoproject/media/reports'
		# outfilepath = os.path.join( outfiledir, outfilename )


		# # imgdata = cStringIO.StringIO()
		# # fig.savefig(imgdata, format='png')
		# # imgdata.seek(0)  # rewind the data

		# Image = ImageReader(fig)
		# filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list+".png")

		# def get_python_image():

		# 	if not os.path.exists(filename) :
		# 		response = print("no picture")
		# 		f = open(filename, 'w')
		# 		f.write(response.read())
		# 		f.close()

		# get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
#		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report2.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report2.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"

	return response

@login_required(login_url='account:login')
def try_analysis3_pdf(request, pk):

	#CREATE BYTSTREAM BUFFER
	# buf=io.BytesIO()
	# #create canvas 
	# c= canvas.Canvas (buf,pagesize=letter, bottomup=0)
	# #text objek di canvas
	# textob=c.beginText()
	# textob.setTextOrigin(inch,inch)
	# textob.setFont("Helvetica", 14)

	#logic data analysis
	nilai_k = int(request.POST.get('nilai_k_select',5))
	#conver into dataframe
	listdata = ListData.objects.get(id=pk)
	entrydata = EntryData.objects.filter(id_list=pk)


	if len(entrydata)>0:
		#ed_df= pd.DataFrame(entrydata.values())
		ed_data=[]
		for ed in entrydata:
			obj={
			'product': ed.product.name,
			'product_id': ed.product_id,
			'kuantitas_terjual': ed.kuantitas_terjual,
			'jumlah_transaksi': ed.jumlah_transaksi,
			'hari_periode':ed.hari_periode,
			'stok_awal': ed.stok_awal,
			'stok_akhir': ed.stok_akhir,
			'produk_rusak': ed.produk_rusak,
			'tor': ed.tor,
			'wsp': ed.wsp,
			}
			ed_data.append(obj)

		entrydata_df=pd.DataFrame(ed_data)
		#print(entrydata_df)

		column_names = [
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp',

		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, column_names])
		#print(x_array)
		#print("-------------")

		#normalisasi data
		x_scaledd = zscore(x_array, ddof=1)
		x_scaled=np.nan_to_num(x_scaledd)
		#print(x_scaled)
		norm_df=pd.DataFrame(x_scaled)
		json_records = norm_df.reset_index().to_json(orient ='records')
		arr4 = []
		arr4 = json.loads(json_records)
		#print(arr4)
		# Menentukan kluster dari data	
		KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
		#print("-------------")	
		#print(KM_5_clusters.cluster_centers_)# append labels to points

		# Menambahkan kolom "kluster" dalam data frame
		entrydata_df['cluster'] = KM_5_clusters.labels_
		#print("-------------")
		# print (entrydata_df['cluster'])
		# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
		# print("-------------")
		# print (product_df)
		#display ccenter
		c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
		json_records = c.reset_index().to_json(orient ='records')
		arr3 = []
		arr3 = json.loads(json_records)

		ccloc=KM_5_clusters.medoid_indices_

		#display_data dan hasil cluster
		cns = [
		   'product',
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp',
	 	   'cluster'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, cns])
		json_records = entrydata_df.reset_index().to_json(orient ='records')
		arr = []
		arr = json.loads(json_records)
		#print("-------------")
		# print(arr)
	    #silhouette score average for all of the cluster
		labels= entrydata_df['cluster']

		s_avg= metrics.silhouette_score(x_scaled, labels)
		#print("-------------")
		#print('Silhouette Score:', s_avg)

	    #silhouette score average for each clusters
	    #silhouette score for each data (idk if i can do this )
	    #graph
		#chart= get_plot(norm_df,pk)
		a=entrydata_df.loc[:, column_names]
		bb=zscore(a, ddof=1)
		cb=np.nan_to_num(bb)
		b=pd.DataFrame(cb)
		json_records = a.reset_index().to_json(orient ='records')
		ar2 = []
		ar2 = json.loads(json_records) 




		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		namalist  = "Nama List Data: "+ listdata.nama_list
		nilaikterpilih = "Nilai k: "+ request.POST.get('nilai_k_select',"5")
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		TaTitle = "Tabel Profiling Cluster"
		TaDesc= "Berikut hasil profiling tiap cluster dari nilai rata-rata variabel "	
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]

		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def body(txt, style=ParaStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para, s]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = p(nilaikterpilih)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(namalist, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		tat=header(TaTitle)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		myabstract = p(Abstract)
		t1d=body(T1Desc)
		t2d=body(T2Desc)
		tad=body(TaDesc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		ta_info= [tat, tad]
		# df buat tabel profiling cluster
		#gabung semua cluster
		meanniee= entrydata_df.groupby(['cluster']).agg("mean")
		meannie=pd.DataFrame(meanniee).iloc[:, 6:9].reset_index()
		#print(meannie)
		rpdtf=[meannie.columns[:,].values.astype(str).tolist()] + meannie.values.tolist()
		tf = Table(rpdtf, colWidths=[82,82],repeatRows=1);
		tf.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))		
		# #c0
		# df_new0 = entrydata_df.loc[entrydata_df['cluster'] == 0]
		# mean00=df_new0.iloc[:, 7:11] .mean()
		# mean0=pd.DataFrame(mean00)
		# mean000=pd.DataFrame(mean00).T.values.tolist()
		# rpdta= [mean0.index.tolist()]+ mean000
		# ta = Table(rpdta, colWidths=[82,82],repeatRows=1);
		# ta.setStyle (TableStyle([
	 #                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	 #                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	 #                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	 #                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	 #                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	 #                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		# #c1
		# df_new1 = entrydata_df.loc[entrydata_df['cluster'] == 1]
		# mean11=df_new1.iloc[:, 7:11] .mean()
		# mean1=pd.DataFrame(mean11)
		# mean111=pd.DataFrame(mean11).T.values.tolist()
		# rpdtb= [mean1.index.tolist()]+ mean111
		# tb = Table(rpdtb, colWidths=[82,82],repeatRows=1);
		# tb.setStyle (TableStyle([
	 #                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	 #                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	 #                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	 #                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	 #                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	 #                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		# #c2
		# df_new2 = entrydata_df.loc[entrydata_df['cluster'] == 2]
		# mean22=df_new2.iloc[:, 7:11] .mean()
		# mean2=pd.DataFrame(mean22)
		# mean222=pd.DataFrame(mean22).T.values.tolist()
		# rpdtc= [mean2.index.tolist()]+ mean222
		# tc = Table(rpdtc, colWidths=[82,82],repeatRows=1);
		# tc.setStyle (TableStyle([
	 #                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	 #                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	 #                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	 #                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	 #                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	 #                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		# #c3
		# df_new3 = entrydata_df.loc[entrydata_df['cluster'] == 3]
		# mean33=df_new3.iloc[:, 7:11] .mean()
		# mean3=pd.DataFrame(mean33)
		# mean333=pd.DataFrame(mean33).T.values.tolist()
		# rpdtd= [mean3.index.tolist()]+ mean333
		# td = Table(rpdtd, colWidths=[82,82],repeatRows=1);
		# td.setStyle (TableStyle([
	 #                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	 #                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	 #                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	 #                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	 #                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	 #                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		# #c4
		# df_new4 = entrydata_df.loc[entrydata_df['cluster'] == 4]
		# mean44=df_new4.iloc[:, 7:11] .mean()
		# mean4=pd.DataFrame(mean44)
		# mean444=pd.DataFrame(mean44).T.values.tolist()
		# rpdte= [mean4.index.tolist()]+ mean444
		# te = Table(rpdte, colWidths=[82,82],repeatRows=1);
		# te.setStyle (TableStyle([
	 #                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	 #                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	 #                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	 #                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	 #                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	 #                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dfn=entrydata_df.loc[:, cns].sort_values('cluster').rename(columns = {'product':'Produk', 'produk_rusak': 'Produk Rusak', 'tor' : 'TOR', 'wsp' : 'WSP ', 'cluster': 'Cluster'}) 
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		xar = np.array(entrydata_df.loc[:, column_names])
		axsc = zscore(xar, ddof=1)
		xsc=np.nan_to_num(axsc)
		# rpdt=np.array(dfn).tolist()
		t1 = Table(rpdt, colWidths=[82,82],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		c2=dfn.loc[KM_5_clusters.medoid_indices_]
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		labels= entrydata_df['cluster']
		sscore=float(metrics.silhouette_score(xsc, labels))
		teksket="Silhouette Score :"
		ket= p(teksket)
		t3_info= [ket]
		score=pd.DataFrame(columns = ['Silhouette Score'])
		s_score=score.append({'Silhouette Score': sscore}, ignore_index = True)
		rpdt3=s_score.values.tolist()
		t3 = Table(rpdt3, colWidths=[20,20], hAlign='LEFT');
		print(rpdt3)
		chart_info=[ctitle]
		buffer = io.BytesIO()

		filename = os.path.join(settings.MEDIA_ROOT,listdata.nama_list + str(listdata.id)+request.user.username+"analisis 3"+".png")

		def get_python_image():

			if not os.path.exists(filename) :
				response = print("no picture")
				f = open(filename, 'w')
				f.write(response.read())
				f.close()

		get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter, rightMargin=15, leftMargin=15)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(ta_info)
		element.append(tf)
		element.extend(t2_info)
		element.append(t2)
		element.append(PageBreak())
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
		element.extend(t3_info)
		element.append(t3)
		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report3.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report3.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"



	else:



		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		URL = "Nama List Data: "+ listdata.nama_list
		email = "Tidak ada data"
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]


		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = header(URL, sep=0.1, style=ParaStyle)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(email, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		t3= p("Tidak Ada Data. Tidak Ada Visualisasi Silhouette Score")
		myabstract = p(Abstract)
		t1d=p(T1Desc)
		t2d=p(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		chart_info=[ctitle, t3]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dc=pd.DataFrame(columns = ['Produk', 'Produk Rusak','TOR', 'WSP' ,  'Cluster']) 
		dfn = dc.append({'Produk': 'Tidak ada Data', 'Produk Rusak' : 'Tidak ada Data','TOR' : 'Tidak ada Data', 'WSP' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		t1 = Table(rpdt, colWidths=[75,75],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		dc2=pd.DataFrame(columns = ['Produk', 'Produk Rusak','TOR', 'WSP',  'Cluster']) 
		c2= dc2.append({'Produk': 'Tidak ada Data', 'Produk Rusak': 'Tidak ada Data','TOR' : 'Tidak ada Data', 'WSP' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		buffer = io.BytesIO()


		# outfilename = listdata.nama_list+".pdf"
		# outfiledir = 'webprojectsnew/lenkoproject/media/reports'
		# outfilepath = os.path.join( outfiledir, outfilename )


		# # imgdata = cStringIO.StringIO()
		# # fig.savefig(imgdata, format='png')
		# # imgdata.seek(0)  # rewind the data

		# Image = ImageReader(fig)
		# filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list+".png")

		# def get_python_image():

		# 	if not os.path.exists(filename) :
		# 		response = print("no picture")
		# 		f = open(filename, 'w')
		# 		f.write(response.read())
		# 		f.close()

		# get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
#		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report3.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report3.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"

	return response
# class flowable_fig(reportlab.platypus.Flowable):
#     def __init__(self, imgdata):
#         reportlab.platypus.Flowable.__init__(self)
#         self.img = reportlab.lib.utils.ImageReader(imgdata)

#     def draw(self):
#         self.canv.drawImage(self.img, 0, 0, height = -2*inch, width=4*inch)
#         # http://www.reportlab.com/apis/reportlab/2.4/pdfgen.html
@login_required(login_url='account:login')
def analysis_pdf(request, pk):

	#CREATE BYTSTREAM BUFFER
	# buf=io.BytesIO()
	# #create canvas 
	# c= canvas.Canvas (buf,pagesize=letter, bottomup=0)
	# #text objek di canvas
	# textob=c.beginText()
	# textob.setTextOrigin(inch,inch)
	# textob.setFont("Helvetica", 14)

	#logic data analysis
	nilai_k = 5
	#conver into dataframe
	listdata = ListData.objects.get(id=pk)
	entrydata = EntryData.objects.filter(id_list=pk)


	if len(entrydata)>0:
		#ed_df= pd.DataFrame(entrydata.values())
		ed_data=[]
		for ed in entrydata:
			obj={
			'product': ed.product.name,
			'product_id': ed.product_id,
			'kuantitas_terjual': ed.kuantitas_terjual,
			'jumlah_transaksi': ed.jumlah_transaksi,
			'hari_periode':ed.hari_periode,
			'stok_awal': ed.stok_awal,
			'stok_akhir': ed.stok_akhir,
			'produk_rusak': ed.produk_rusak,
			'tor': ed.tor,
			'wsp': ed.wsp,
			}
			ed_data.append(obj)

		entrydata_df=pd.DataFrame(ed_data)
		#print(entrydata_df)

		column_names = [
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, column_names])
		#print(x_array)
		#print("-------------")

		#normalisasi data
		x_scaled = zscore(x_array, ddof=1)
		#print(x_scaled)
		norm_df=pd.DataFrame(x_scaled)
		json_records = norm_df.reset_index().to_json(orient ='records')
		arr4 = []
		arr4 = json.loads(json_records)
		#print(arr4)
		# Menentukan kluster dari data	
		KM_5_clusters = KMedoids(n_clusters=nilai_k, init='k-medoids++', random_state=0).fit(x_scaled) # initialise and fit K-Means model
		#print("-------------")	
		#print(KM_5_clusters.cluster_centers_)# append labels to points

		# Menambahkan kolom "kluster" dalam data frame
		entrydata_df['cluster'] = KM_5_clusters.labels_
		#print("-------------")
		# print (entrydata_df['cluster'])
		# product_df= pd.DataFrame(Product.objects.filter(id=entrydata_df.product_id).values())
		# print("-------------")
		# print (product_df)
		#display ccenter
		c=entrydata_df.loc[KM_5_clusters.medoid_indices_]
		json_records = c.reset_index().to_json(orient ='records')
		arr3 = []
		arr3 = json.loads(json_records)

		ccloc=KM_5_clusters.medoid_indices_

		#display_data dan hasil cluster
		cns = [
		   'product',
	 	   'kuantitas_terjual',
	 	   'jumlah_transaksi',
	 	   'produk_rusak',
	 	   'tor',
	 	   'wsp',
	 	   'cluster'
		]
		#ambil kolom data yang dipilih sebagai parameter
		x_array = np.array(entrydata_df.loc[:, cns])
		json_records = entrydata_df.reset_index().to_json(orient ='records')
		arr = []
		arr = json.loads(json_records)
		#print("-------------")
		# print(arr)
	    #silhouette score average for all of the cluster
		labels= entrydata_df['cluster']
		s_avg= metrics.silhouette_score(x_scaled, labels)
		#print("-------------")
		#print('Silhouette Score:', s_avg)

	    #silhouette score average for each clusters
	    #silhouette score for each data (idk if i can do this )
	    #graph
		#chart= get_plot(norm_df,pk)
		a=entrydata_df.loc[:, column_names]
		b=zscore(a, ddof=1)
		json_records = a.reset_index().to_json(orient ='records')
		ar2 = []
		ar2 = json.loads(json_records) 




		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		URL = "http://protocolostomy.com"
		email = "bkjones@gmail.com"
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]

		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def body(txt, style=ParaStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para, s]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = header(URL, sep=0.1, style=ParaStyle)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(email, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		myabstract = p(Abstract)
		t1d=body(T1Desc)
		t2d=body(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dfn=entrydata_df.loc[:, cns].sort_values('cluster').rename(columns = {'product':'Produk', 'kuantitas_terjual': 'Kuantitas Terjual', 'jumlah_transaksi': 'Jumlah Transaksi', 'produk_rusak': 'Produk Rusak', 'tor': 'TOR', 'wsp': 'WSP', 'cluster': 'Cluster'}) 
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		xar = np.array(entrydata_df.loc[:, column_names])
		axsc = zscore(xar, ddof=1)
		xsc=np.nan_to_num(axsc)
		# rpdt=np.array(dfn).tolist()
		t1 = Table(rpdt, colWidths=[82,82],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		c2=dfn.loc[KM_5_clusters.medoid_indices_]
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#DAF7A6")),
	                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
	                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		labels= entrydata_df['cluster']
		sscore=float(metrics.silhouette_score(xsc, labels))
		teksket="Silhouette Score :"
		ket= p(teksket)
		t3_info= [ket]
		score=pd.DataFrame(columns = ['Silhouette Score'])
		s_score=score.append({'Silhouette Score': sscore}, ignore_index = True)
		rpdt3=s_score.values.tolist()
		t3 = Table(rpdt3, colWidths=[20,20], hAlign='LEFT');
		print(rpdt3)
		chart_info=[ctitle]
		buffer = io.BytesIO()

		filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list+str(listdata.id)+".png")

		def get_python_image():

			if not os.path.exists(filename) :
				response = print("no picture")
				f = open(filename, 'w')
				f.write(response.read())
				f.close()

		get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter, rightMargin=15, leftMargin=15)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.append(PageBreak())
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
		element.extend(t3_info)
		element.append(t3)
		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"



	else:



		styles = getSampleStyleSheet()
		Title = "Laporan Pengelompokan Produk PT. Lenko Surya Perkasa Sidoarjo" + " "+ listdata.nama_list
		Author = "Dibuat Oleh" + ": "+ request.user.username
		URL = "http://protocolostomy.com"
		email = "bkjones@gmail.com"
		Abstract = """Berikut adalah Medoid dan Hasil Pengelompokan Data Produk PT. Lenko Surya Perkasa pada""" + " "+ listdata.nama_list
		T2Title = "Tabel Medoid Data Produk"
		T2Desc= "Karakteristik produk dapat dilihat dari karakteristik medoid tiap cluster. "
		T1Title = "Tabel Hasil Pengelompokan Produk"
		T1Desc= "Produk yang telah dikelompokkan dapat dilihat pada tabel dibawah. Tabel telah diurutkan berdasarkan cluster. "		
		charttitle = "Visualisasi Silhouette Score Data Produk"
		HeaderStyle = styles["Heading1"]
		ParaStyle = styles["Normal"]
		PreStyle = styles["Code"]


		def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
			s = Spacer(0.2*inch, sep*inch)
			para = klass(txt, style)
			sect = [s, para]
			result = KeepTogether(sect)
			return result
		def p(txt):
			return header(txt, style=ParaStyle, sep=0.1)


		mytitle = header(Title)
		mysite = header(URL, sep=0.1, style=ParaStyle)
		myname = header(Author, sep=0.1, style=ParaStyle)
		mymail = header(email, sep=0.1, style=ParaStyle)
		t1t=header(T1Title)
		t2t=header(T2Title)
		ctitle=header(charttitle)
		abstract_title = header("Hasil Pengelompokan Data Produk")
		t3= p("Tidak Ada Data. Tidak Ada Visualisasi Silhouette Score")
		myabstract = p(Abstract)
		t1d=p(T1Desc)
		t2d=p(T2Desc)
		head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
		t1_info= [t1t, t1d]
		t2_info= [t2t, t2d]
		chart_info=[ctitle, t3]
		#t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
		dc=pd.DataFrame(columns = ['Produk','Kuantitas Terjual', 'Jumlah Transaksi', 'Produk Rusak',  'TOR',  'WSP',  'Cluster']) 
		dfn = dc.append({'Produk': 'Tidak ada Data','Kuantitas Terjual' : 'Tidak ada Data', 'Jumlah Transaksi' : 'Tidak ada Data', 'Produk Rusak' : 'Tidak ada Data',  'TOR' : 'Tidak ada Data',  'WSP' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		#nama kolom + datanya 
		rpdt=[dfn.columns[:,].values.astype(str).tolist()] + dfn.values.tolist()
		t1 = Table(rpdt, colWidths=[75,75],repeatRows=1);
		t1.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

		dc2=pd.DataFrame(columns = ['Produk','Kuantitas Terjual', 'Jumlah Transaksi', 'Produk Rusak',  'TOR',  'WSP',  'Cluster']) 
		c2= dc2.append({'Produk': 'Tidak ada Data','Kuantitas Terjual' : 'Tidak ada Data', 'Jumlah Transaksi' : 'Tidak ada Data', 'Produk Rusak' : 'Tidak ada Data',  'TOR' : 'Tidak ada Data',  'WSP' : 'Tidak ada Data',  'Cluster' : 'Tidak ada Data'}, 
                ignore_index = True)
		rpdt2=[c2.columns[:,].values.astype(str).tolist()] + c2.values.tolist()
		t2 = Table(rpdt2, colWidths=[75,75],repeatRows=1);
		t2.setStyle (TableStyle([
	                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
	                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
	                       ('FONTSIZE', (0,0), (-1, -1), 5.5),
	                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))
		ftd = [[t1],[t2]]
		overallTable = Table(ftd)
		buffer = io.BytesIO()


		# outfilename = listdata.nama_list+".pdf"
		# outfiledir = 'webprojectsnew/lenkoproject/media/reports'
		# outfilepath = os.path.join( outfiledir, outfilename )


		# # imgdata = cStringIO.StringIO()
		# # fig.savefig(imgdata, format='png')
		# # imgdata.seek(0)  # rewind the data

		# Image = ImageReader(fig)
		# filename = os.path.join(settings.MEDIA_ROOT, listdata.nama_list+".png")

		# def get_python_image():

		# 	if not os.path.exists(filename) :
		# 		response = print("no picture")
		# 		f = open(filename, 'w')
		# 		f.write(response.read())
		# 		f.close()

		# get_python_image()

		doc = SimpleDocTemplate(buffer, pagesizes=letter)
		
		element = []
		element.append(Image('logo.png'))
		element.append(Image('line.png', 20*cm, 2*cm ))		
		element.extend(head_info)
		element.extend(t2_info)
		element.append(t2)
		element.extend(t1_info)
		element.append(t1)
		element.extend(chart_info)
#		element.append(Image(filename, width=300, height=150))



		doc.build(element)

		buffer.seek(0)
		pdf: bytes = buffer.getvalue()

		r_name=listdata.nama_list+ " id: "+ str(listdata.id)+".pdf"
		aut=AdminProfile.objects.get(user=request.user)
		list_obj= ListData.objects.get(id=pk)
		file_data = ContentFile(pdf)
		report_profile = Report.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
		field=Report.objects.get(list_id=list_obj, author=aut)
            # get users enrolment_pdf field

            # save the generated pdf to the user in the database
		# report_profile.save()
		# field=report_profile.report_file
		field.report_file.save(listdata.nama_list+ " id: "+ str(listdata.id)+".pdf", file_data , save=False)
		field.save()
		field.activated=True
		field.save()
		#response = FileResponse(pdf, filename=listdata.nama_list+".pdf")
		response = HttpResponse(content_type='application/pdf')
		response.write(buffer.getvalue())
		response['Content-Disposition'] = 'attachment; filename=%s' % listdata.nama_list+".pdf"

	return response

# def generate_user_pdf(request,pk):
# 	listdata = ListData.objects.get(id=pk)
# 	aut=AdminProfile.objects.get(user=request.user)
# 	# generate pdf containing all answers
# 	report_file = analysis_pdf(request,pk)

#             # get users enrolment_pdf field
#             # temp hard-coded
#             #ini error nya gabisa match soalnya emang blm ada report samsek, match dari mana, maybe ini bisa nanti buat cek dah ada report atau blm 

# 	r_name=listdata.nama_list+".pdf"
# 	list_obj= ListData.objects.get(id=pk)
# 	report_profile = Report.objects.get_or_create(report_name=r_name, list_id=list_obj, author=aut)
# #	field = report_profile.report_file

# 	# save the generated pdf to the user in the database
# 	file_data = ContentFile(report_file)
# 	report_profile.report_file.save(listdata.nama_list+".pdf", file_data , save=False)
# 	report_profil.save()
