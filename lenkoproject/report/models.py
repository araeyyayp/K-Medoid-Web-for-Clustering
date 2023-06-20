from django.db import models
from adminprofiles.models import AdminProfile
from inventdata.models import ListData, EntryData, CSV
from adminprofiles.models import AdminProfile
from django.http import HttpResponse
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import os.path, time

# Create your models here.
class Report (models.Model):
	report_name= models.CharField(max_length=100)
	report_file= models.FileField(upload_to='report/', max_length=100)
	list_id=models.ForeignKey('inventdata.ListData', on_delete=models.CASCADE)
	author= models.ForeignKey (AdminProfile, on_delete=models.CASCADE)
	created=models.DateTimeField (auto_now_add=True)
	updated=models.DateTimeField (auto_now=True)
	activated=models.BooleanField(default=False)

	def __str__(self):
		return str(self.report_name)

	def get_absolute_url(self):
		return self.report_file.url

class Report2 (models.Model):
	report_name= models.CharField(max_length=100)
	report_file= models.FileField(upload_to='report2/', max_length=100)
	list_id=models.ForeignKey('inventdata.ListData', on_delete=models.CASCADE)
	author= models.ForeignKey (AdminProfile, on_delete=models.CASCADE)
	created=models.DateTimeField (auto_now_add=True)
	updated=models.DateTimeField (auto_now_add=True)
	activated=models.BooleanField(default=False)

	def __str__(self):
		return str(self.report_name)
		
	def get_absolute_url(self):
		return self.report_file.url

class Report3 (models.Model):
	report_name= models.CharField(max_length=100)
	report_file= models.FileField(upload_to='report3/', max_length=100)
	list_id=models.ForeignKey('inventdata.ListData', on_delete=models.CASCADE)
	author= models.ForeignKey (AdminProfile, on_delete=models.CASCADE)
	created=models.DateTimeField (auto_now_add=True)
	updated=models.DateTimeField (auto_now_add=True)
	activated=models.BooleanField(default=False)

	def __str__(self):
		return str(self.report_name)

	def get_absolute_url(self):
		return self.report_file.url