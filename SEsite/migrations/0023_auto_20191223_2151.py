# Generated by Django 3.0 on 2019-12-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEsite', '0022_auto_20191223_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='pushTime',
            field=models.DateField(auto_now_add=True, verbose_name='pushTime'),
        ),
    ]