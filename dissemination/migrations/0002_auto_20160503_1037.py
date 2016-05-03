# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dissemination', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='external',
            name='author',
            field=models.ManyToManyField(to='person.Person', null=True, verbose_name='Author', blank=True),
            preserve_default=True,
        ),
    ]
