# Generated by Django 3.2.7 on 2021-11-16 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventdata', '0007_entrydata_sisa_produk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entrydata',
            old_name='sisa_produk_akhir',
            new_name='stok_akhir',
        ),
        migrations.RenameField(
            model_name='entrydata',
            old_name='sisa_produk_awal',
            new_name='stok_awal',
        ),
    ]