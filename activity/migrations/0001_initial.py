# Generated by Django 2.2.5 on 2019-09-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
                'ordering': ('url',),
            },
        ),
        migrations.CreateModel(
            name='ProjectActivities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('type_of_activity', models.CharField(
                    blank=True,
                    choices=[('t', 'Training Program'), ('m', 'Meeting'), ('s', 'Seminar')],
                    max_length=1,
                    verbose_name='Type of activity')),
            ],
            options={
                'ordering': ('type_of_activity', 'title'),
            },
        ),
        migrations.CreateModel(
            name='SeminarType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('image', models.ImageField(
                    blank=True,
                    help_text='Logo for poster. We recommend an image with size 400x100.',
                    null=True,
                    upload_to='banners/',
                    verbose_name='Image')),
                ('qr_code', models.ImageField(
                    blank=True,
                    help_text='QR code with link to some page.',
                    null=True,
                    upload_to='qr_code/',
                    verbose_name='QR Code')),
            ],
            options={
                'verbose_name': 'Type of seminar',
                'verbose_name_plural': 'Types of seminar',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('projectactivities_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='activity.ProjectActivities')),
                ('broad_audience', models.BooleanField(default=False, verbose_name='Broad audience?')),
                ('cepid_event', models.BooleanField(default=False, verbose_name='Organized by CEPID?')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='banners/', verbose_name='Banner')),
            ],
            options={
                'verbose_name': 'Meeting',
                'verbose_name_plural': 'Meetings',
                'ordering': ('-start_date',),
            },
            bases=('activity.projectactivities',),
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('projectactivities_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='activity.ProjectActivities')),
                ('international_guest_lecturer', models.BooleanField(
                    default=False,
                    verbose_name='International guest lecturer?')),
                ('abstract', models.TextField(blank=True, null=True, verbose_name='Abstract')),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Time')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='', verbose_name='Attachment')),
                ('room', models.CharField(blank=True, max_length=255, null=True, verbose_name='Room')),
            ],
            options={
                'verbose_name': 'Seminar',
                'verbose_name_plural': 'Seminars',
                'ordering': ('-date',),
            },
            bases=('activity.projectactivities',),
        ),
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('projectactivities_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='activity.ProjectActivities')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('duration', models.CharField(
                    choices=[('1h', '1h'),
                             ('1h30', '1h30'),
                             ('2h', '2h'),
                             ('2h30', '2h30'),
                             ('3h', '3h'),
                             ('3h30', '3h30'),
                             ('4h', '4h'),
                             ('4h30', '4h30'),
                             ('5h', '5h'),
                             ('5h30', '5h30'),
                             ('6h', '6h'),
                             ('6h30', '6h30'),
                             ('7h', '7h'),
                             ('7h30', '7h30'),
                             ('8h', '8h'),
                             ('8h30', '8h30'),
                             ('9h', '9h'),
                             ('9h30', '9h30'),
                             ('10h', '10h'),
                             ('Other', 'Other duration time')],
                    max_length=5,
                    verbose_name='Duration')),
                ('other_duration', models.CharField(
                    blank=True,
                    help_text='E.g.: 11h or 11h30',
                    max_length=5,
                    null=True,
                    verbose_name='Other duration time')),
                ('number_of_participants', models.IntegerField(
                    blank=True,
                    null=True,
                    verbose_name='Number of participants')),
            ],
            options={
                'verbose_name': 'Training Program',
                'verbose_name_plural': 'Training Programs',
                'ordering': ('-start_date',),
            },
            bases=('activity.projectactivities',),
        ),
    ]
