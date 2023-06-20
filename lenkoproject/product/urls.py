from django.urls import path
from . import views
from .views import (
	ProductView,


)

app_name= 'product'

urlpatterns = [
#	path('upload/', views.simple_upload, name="upload"),
	path('', views.producthome, name="producthome"),
	path('add/', views.addproduct, name="add"),
	path('list/', ProductView.as_view(), name="list"),
	path('list/delete/<int:pk>/', views.deleteproduct, name="delete-product"),
	path('list/edit/<int:pk>', views.editproduct, name="edit-product"),
	path('list/upload-product', views.uploadproduct, name="upload-product"),
	]