# Generated by Django 3.2.7 on 2021-09-28 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventdata', '0003_alter_entrydata_hari_periode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrydata',
            name='id_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry', to='inventdata.listdata'),
        ),
    ]
