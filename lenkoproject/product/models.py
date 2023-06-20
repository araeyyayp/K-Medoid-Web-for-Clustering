from django.db import models

# Create your models here.
class Product (models.Model):
	name = models.CharField(max_length=50)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.name}"

class Csv (models.Model):
	file_name= models.FileField(upload_to='product/', max_length=100)
	uploaded= models.DateTimeField(auto_now_add=True)
	activated=models.BooleanField(default=False)

	def __str__(self):
		return "File id: {}".format(self.id)