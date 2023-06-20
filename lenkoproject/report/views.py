from django.shortcuts import render
from .models import Report, Report2, Report3
from django.views.generic import ListView
from django.shortcuts import redirect
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.

class ReportDataView(ListView):
	model= Report
	template_name= 'report/reportdatalist.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['listnum'] = Report.objects.all().count()
		context['report2'] = Report2.objects.all()
		context['report3'] = Report3.objects.all()
		context['listnum2'] = Report2.objects.all().count()
		context['listnum3'] = Report3.objects.all().count()	
		return context

@login_required(login_url='account:login')
def deletereport(request,pk):
	product= Report.objects.filter(id=pk).last()
	product.delete()
	return redirect ('report:reportlist')

@login_required(login_url='account:login')
def deletereport2 (request,pk):
	product= Report2.objects.filter(id=pk).last()
	product.delete()
	return redirect ('report:reportlist')
	
@login_required(login_url='account:login')
def deletereport3 (request,pk):
	product= Report3.objects.filter(id=pk).last()
	product.delete()
	return redirect ('report:reportlist')