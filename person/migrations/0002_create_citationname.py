# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitationName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name in bibliographic citation')),
                ('default_name', models.BooleanField(default=False, max_length=3, verbose_name='Default name?',
                                                     choices=[(True, 'Yes'), (False, 'No')])),
                ('person', models.ForeignKey(verbose_name='Name', to='person.Person')),
            ],
            options={
                'ordering': ('person',),
                'verbose_name': 'Citation name',
                'verbose_name_plural': 'Citation name',
            },
            bases=(models.Model,),
        ),
    ]
