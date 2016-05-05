# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
        ('cities_light', '0006_compensate_for_0003_bytestring_bug'),
        ('person', '0003_remove_person_citation_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScientificMission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departure', models.DateTimeField(verbose_name='Departure')),
                ('arrival', models.DateTimeField(verbose_name='Arrival')),
                ('amount_paid', models.DecimalField(verbose_name='Amount paid', max_digits=10, decimal_places=2)),
                ('destination_city', models.ForeignKey(related_name='destination_city', verbose_name='City of destination', to='cities_light.City')),
                ('destination_country', models.ForeignKey(related_name='destination_country', verbose_name='Country of destination', to='cities_light.Country')),
            ],
            options={
                'ordering': ('person',),
                'verbose_name': 'Daily stipend',
                'verbose_name_plural': 'Daily stipends',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mission', models.CharField(max_length=255, null=True, verbose_name='Scientific Mission', blank=True)),
            ],
            options={
                'ordering': ('mission',),
                'verbose_name': 'Type of scientific mission',
                'verbose_name_plural': 'Types of scientific mission',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scientificmission',
            name='mission',
            field=models.ForeignKey(verbose_name='Mission', blank=True, to='scientific_mission.Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scientificmission',
            name='origin_city',
            field=models.ForeignKey(verbose_name='City of origin', to='cities_light.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scientificmission',
            name='origin_country',
            field=models.ForeignKey(verbose_name='Country of origin', to='cities_light.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scientificmission',
            name='person',
            field=models.ForeignKey(verbose_name='Paid to', to='person.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scientificmission',
            name='project_activity',
            field=models.ForeignKey(verbose_name='Project activity', blank=True, to='activity.ProjectActivities', null=True),
            preserve_default=True,
        ),
    ]
