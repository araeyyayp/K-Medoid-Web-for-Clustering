from django.urls import path
from . import views
from .views import (
	ReportDataView,


)

app_name= 'report'

urlpatterns = [
#	path('upload/', views.simple_upload, name="upload"),
	path('list/', ReportDataView.as_view(), name="reportlist"),
	path('list/delete/<int:pk>/', views.deletereport, name="delete-report"),
	path('list/delete2/<int:pk>/', views.deletereport2, name="delete-report2"),
	path('list/delete3/<int:pk>/', views.deletereport3, name="delete-report3"),
	#path('edit/',views.editentry, name="edit"),
	]