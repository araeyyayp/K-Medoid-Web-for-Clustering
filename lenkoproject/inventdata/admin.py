from django.contrib import admin
from .models import ListData, EntryData, CSV
# Register your models here.
admin.site.register(ListData)
admin.site.register(EntryData)
admin.site.register(CSV)