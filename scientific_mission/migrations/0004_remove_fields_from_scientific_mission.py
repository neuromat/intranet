# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-23 20:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scientific_mission', '0003_copy_data_to_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scientificmission',
            name='arrival',
        ),
        migrations.RemoveField(
            model_name='scientificmission',
            name='departure',
        ),
        migrations.RemoveField(
            model_name='scientificmission',
            name='origin_city',
        ),
    ]
