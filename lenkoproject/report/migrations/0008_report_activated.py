# Generated by Django 3.2.7 on 2021-11-04 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0007_alter_report_report_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
