# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
                'ordering': ('url',),
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectActivities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('type_of_activity', models.CharField(blank=True, max_length=1, verbose_name='Type of activity', choices=[(b't', 'Training Program'), (b'm', 'Meeting'), (b's', 'Seminar')])),
            ],
            options={
                'ordering': ('type_of_activity', 'title'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('projectactivities_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='activity.ProjectActivities')),
                ('broad_audience', models.BooleanField(default=False, verbose_name='Broad audience?')),
                ('cepid_event', models.BooleanField(default=False, verbose_name='Organized by NeuroMat?')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('participant', models.ManyToManyField(to='person.Person', null=True, verbose_name='Participant', blank=True)),
            ],
            options={
                'ordering': ('-start_date',),
                'verbose_name': 'Meeting',
                'verbose_name_plural': 'Meetings',
            },
            bases=('activity.projectactivities',),
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('projectactivities_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='activity.ProjectActivities')),
                ('international_guest_lecturer', models.BooleanField(default=False, verbose_name='International guest lecturer?')),
                ('abstract', models.TextField(null=True, verbose_name='Abstract', blank=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(null=True, verbose_name='Time', blank=True)),
                ('attachment', models.FileField(upload_to=b'', null=True, verbose_name='Attachment', blank=True)),
                ('room', models.CharField(max_length=255, null=True, verbose_name='Room', blank=True)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Seminar',
                'verbose_name_plural': 'Seminars',
            },
            bases=('activity.projectactivities',),
        ),
        migrations.CreateModel(
            name='SeminarType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Type of seminar',
                'verbose_name_plural': 'Types of seminar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('projectactivities_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='activity.ProjectActivities')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('duration', models.CharField(max_length=5, verbose_name='Duration', choices=[(b'1h', b'1h'), (b'1h30', b'1h30'), (b'2h', b'2h'), (b'2h30', b'2h30'), (b'3h', b'3h'), (b'3h30', b'3h30'), (b'4h', b'4h'), (b'4h30', b'4h30'), (b'5h', b'5h'), (b'5h30', b'5h30'), (b'6h', b'6h'), (b'6h30', b'6h30'), (b'7h', b'7h'), (b'7h30', b'7h30'), (b'8h', b'8h'), (b'8h30', b'8h30'), (b'9h', b'9h'), (b'9h30', b'9h30'), (b'10h', b'10h'), (b'Other', 'Other duration time')])),
                ('other_duration', models.CharField(help_text=b'E.g.: 11h or 11h30', max_length=5, null=True, verbose_name='Other duration time', blank=True)),
                ('number_of_participants', models.IntegerField(null=True, verbose_name='Number of participants', blank=True)),
                ('meeting', models.ForeignKey(verbose_name='Meeting', blank=True, to='activity.Meeting', null=True)),
                ('speaker', models.ManyToManyField(to='person.Person', verbose_name='Speaker')),
            ],
            options={
                'ordering': ('-start_date',),
                'verbose_name': 'Training Program',
                'verbose_name_plural': 'Training Programs',
            },
            bases=('activity.projectactivities',),
        ),
        migrations.AddField(
            model_name='seminar',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='activity.SeminarType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seminar',
            name='meeting',
            field=models.ForeignKey(verbose_name='Meeting', blank=True, to='activity.Meeting', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seminar',
            name='speaker',
            field=models.ManyToManyField(to='person.Person', verbose_name='Speaker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectactivities',
            name='local',
            field=models.ForeignKey(verbose_name='Local', blank=True, to='person.Institution', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='activity',
            field=models.ForeignKey(to='activity.ProjectActivities'),
            preserve_default=True,
        ),
    ]
