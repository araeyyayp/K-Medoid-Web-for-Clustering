from django.urls import path
from . import views
from .views import (
	ListDataView,
	ListDetailView,
	inventdatahome,

)

app_name= 'inventdata'

urlpatterns = [
#	path('upload/', views.simple_upload, name="upload"),
	path('', views.inventdatahome, name="inventdatahome"),
	path('add/', views.addlist, name="add"),
	path('list/', ListDataView.as_view(), name="list"),
	path('list/<int:pk>/', ListDetailView.as_view(), name="detail"),
	path('list/delete/<int:pk>/', views.deletelist, name="delete-list"),
	path('list/edit/<int:pk>/', views.editlist, name="edit-list"),
	path('list/<int:pk>/add-entry', views.entryadd, name="add-entry"),
	path('list/<int:pk>/upload-entry', views.uploadentry, name="upload-entry"),
	path('list/<int:pk>/upload-data-periode', views.uploadperiode, name="upload-data-periode"),
	path('list/<int:pk>/delete/<int:id>', views.deleteentry, name="delete-entry"),
	path('list/<int:pk>/analysis', views.analysis, name="analysis"),
	path('list/<int:pk>/analysis/report', views.analysis_pdf, name="report"),
	path('list/<int:pk>/tryanalysis/report2', views.try_analysis_pdf, name="report2"),
	path('list/<int:pk>/tryanalysis2/tryreport2', views.try_analysis2_pdf, name="tryreport2"),
	path('list/<int:pk>/tryanalysis3/tryreport3', views.try_analysis3_pdf, name="tryreport3"),
	path('list/<int:pk>/tryanalysis', views.tryanalysis, name="try-analysis"),
	path('list/<int:pk>/tryanalysis2', views.tryanalysis2, name="try-analysis2"),
	path('list/<int:pk>/tryanalysis3', views.tryanalysis3, name="try-analysis3"),
	path('list/<int:pk>/edit/<int:identry>', views.editentry, name="edit-entry"),
	#path('edit/',views.editentry, name="edit"),
	]