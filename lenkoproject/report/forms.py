from django import forms
from django.forms import ModelForm
from .models import Report



class PdfForm (forms.ModelForm):
	class Meta:
		model=Report
		fields=['report_name', 'report_file', 'list_id', 'author']