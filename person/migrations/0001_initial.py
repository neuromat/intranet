# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import person.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('acronym', models.CharField(max_length=50, null=True, verbose_name='Acronym', blank=True)),
                ('belongs_to', models.ForeignKey(verbose_name='Belongs to', blank=True, to='person.Institution', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Institutions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstitutionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Type of institution',
                'verbose_name_plural': 'Types of institution',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(unique=True, max_length=255, verbose_name='Full name')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('citation_name', models.CharField(help_text='E.g.: Silva, J.', max_length=255, null=True, verbose_name='Name in bibliographic citation', blank=True)),
                ('rg', models.CharField(max_length=12, null=True, verbose_name='RG', blank=True)),
                ('cpf', models.CharField(blank=True, max_length=15, null=True, verbose_name='CPF', validators=[person.models.validate_cpf])),
                ('passport', models.CharField(max_length=12, null=True, verbose_name='Passport', blank=True)),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Phone', blank=True)),
                ('cellphone', models.CharField(max_length=15, null=True, verbose_name='Cell Phone', blank=True)),
                ('zipcode', models.CharField(max_length=9, null=True, verbose_name='Zip Code', blank=True)),
                ('street', models.CharField(max_length=255, null=True, verbose_name='Address', blank=True)),
                ('street_complement', models.CharField(max_length=255, null=True, verbose_name='Complement', blank=True)),
                ('number', models.CharField(max_length=10, null=True, verbose_name='Number', blank=True)),
                ('district', models.CharField(max_length=255, null=True, verbose_name='District', blank=True)),
                ('city', models.CharField(max_length=255, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=255, null=True, verbose_name='State', blank=True)),
                ('country', models.CharField(max_length=255, null=True, verbose_name='Country', blank=True)),
                ('institution', models.ForeignKey(verbose_name='Institution', blank=True, to='person.Institution', null=True)),
            ],
            options={
                'ordering': ('full_name',),
                'verbose_name': 'Person',
                'verbose_name_plural': 'Person',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ForeignKey(verbose_name='Role', blank=True, to='person.Role', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='institution',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='person.InstitutionType'),
            preserve_default=True,
        ),
    ]
