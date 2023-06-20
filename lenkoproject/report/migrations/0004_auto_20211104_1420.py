# Generated by Django 3.2.7 on 2021-11-04 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventdata', '0006_alter_csv_file_name'),
        ('report', '0003_auto_20211104_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='remarks',
        ),
        migrations.AddField(
            model_name='report',
            name='id_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventdata.listdata'),
        ),
    ]
