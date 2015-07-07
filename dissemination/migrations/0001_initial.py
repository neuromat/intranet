# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dissemination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Date')),
                ('link', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('type_of_media', models.CharField(blank=True, max_length=1, verbose_name='Type of media', choices=[(b'i', 'Internal'), (b'e', 'External')])),
            ],
            options={
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='External',
            fields=[
                ('dissemination_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dissemination.Dissemination')),
                ('author', models.ManyToManyField(to='person.Person', verbose_name='Author')),
            ],
            options={
                'verbose_name': 'External',
                'verbose_name_plural': 'External',
            },
            bases=('dissemination.dissemination',),
        ),
        migrations.CreateModel(
            name='ExternalMediaOutlet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'External media outlet',
                'verbose_name_plural': 'External media outlets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Internal',
            fields=[
                ('dissemination_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dissemination.Dissemination')),
                ('author', models.ManyToManyField(to='person.Person', null=True, verbose_name='Author', blank=True)),
            ],
            options={
                'verbose_name': 'Internal',
                'verbose_name_plural': 'Internal',
            },
            bases=('dissemination.dissemination',),
        ),
        migrations.CreateModel(
            name='InternalMediaOutlet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Internal media outlet',
                'verbose_name_plural': 'Internal media outlets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='internal',
            name='media_outlet',
            field=models.ForeignKey(verbose_name='Media outlet', to='dissemination.InternalMediaOutlet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='external',
            name='media_outlet',
            field=models.ForeignKey(verbose_name='Media outlet', to='dissemination.ExternalMediaOutlet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dissemination',
            name='topic',
            field=models.ManyToManyField(to='dissemination.Topic', null=True, verbose_name='Topic', blank=True),
            preserve_default=True,
        ),
    ]
