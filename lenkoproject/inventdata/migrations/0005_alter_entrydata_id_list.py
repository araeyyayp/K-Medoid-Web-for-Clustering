# Generated by Django 3.2.7 on 2021-09-28 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventdata', '0004_alter_entrydata_id_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrydata',
            name='id_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventdata.listdata'),
        ),
    ]