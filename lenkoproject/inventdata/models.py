from django.db import models
from product.models import Product
from django.shortcuts import reverse

# Create your models here.
class ListData (models.Model):
	nama_list= models.CharField(max_length=30)
	created=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "File id: {}".format(self.id)

	def get_absolute_url (self):
		return reverse ('inventdata:detail', kwargs = {'pk': self.pk})

class EntryData (models.Model):
	product= models.ForeignKey(Product, on_delete=models.CASCADE)
	kuantitas_terjual=models.PositiveIntegerField(default=0)
	jumlah_transaksi=models.IntegerField(default=0)
	produk_rusak=models.IntegerField(default=0)
	sisa_produk= models.IntegerField(default=0)
	stok_awal=models.IntegerField(default=0)
	stok_akhir=models.IntegerField(default=0)
	hari_periode=models.PositiveIntegerField(default=365)
	tor =models.FloatField(blank=True, default=0)
	wsp =models.FloatField(blank=True, default=0)
	id_list=models.ForeignKey(ListData, on_delete=models.CASCADE)
	
	def save (self, *args, **kwargs):
		if (self.kuantitas_terjual==0) or (self.stok_awal==0 and self.stok_akhir==0) or (self.kuantitas_terjual==0 and self.stok_awal==0) or (self.kuantitas_terjual==0 and self.stok_akhir==0) :
			self.tor=0
			self.wsp=0
		else:
			self.tor = self.kuantitas_terjual / ((self.stok_awal+self.stok_akhir)/2)
			self.wsp = self.hari_periode/self.tor 

		return super().save(*args, **kwargs)

	def __str__(self):
		return f"File id: {self.id}, product : {self.product.name}"
		

class CSV (models.Model):
	file_name= models.FileField(upload_to='inventdata/', max_length=100)
	uploaded= models.DateTimeField(auto_now_add=True)
	activated=models.BooleanField(default=False)

	def __str__(self):
		return "File id: {}".format(self.id)