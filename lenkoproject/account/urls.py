from django.urls import path
from . import views

app_name= 'account'
urlpatterns = [
	path('login/', views.loginPage, name="login"), 
	path('register/', views.register, name="register"),
	path('logout/', views.logoutUser, name="logout"),
	path('homepage/', views.homepage, name="homepage"), 
    path('', views.homepage, name="home"),
    path('export-excel/', views.export_excel, name="export-excel"),
    path('export-xls/', views.export_xls, name="export-xls"),
    path('export-excel-tahun/', views.export_excel_tahun, name="export-excel-tahun"),
    path('export-xls-tahun/', views.export_xls_tahun, name="export-xls-tahun"),
    path('export-excel-produk/', views.export_excel_produk, name="export-excel-produk"),
    path('export-xls-produk/', views.export_xls_produk, name="export-xls-produk"),


]