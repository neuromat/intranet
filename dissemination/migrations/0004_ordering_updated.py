# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 18:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dissemination', '0003_null_has_no_effect_on_ManyToManyField'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dissemination',
            options={'ordering': ('-date', 'title')},
        ),
    ]
