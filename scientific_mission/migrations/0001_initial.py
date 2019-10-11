from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('person', '0001_initial'),
        ('activity', '0002_auto_20190911_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission', models.CharField(blank=True, max_length=255, null=True, verbose_name='Scientific Mission')),
            ],
            options={
                'verbose_name': 'Type of scientific mission',
                'verbose_name_plural': 'Types of scientific mission',
                'ordering': ('mission',),
            },
        ),
        migrations.CreateModel(
            name='ScientificMission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount paid')),
                ('date_of_registration', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date')),
                ('destination_city', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='destination_city',
                    to='cities_light.City',
                    verbose_name='City of destination')),
                ('mission', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='scientific_mission.Type',
                    verbose_name='Mission')),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='person.Person',
                    verbose_name='Paid to')),
                ('project_activity', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='activity.ProjectActivities',
                    verbose_name='Project activity')),
            ],
            options={
                'verbose_name': 'Daily stipend',
                'verbose_name_plural': 'Daily stipends',
                'ordering': ('-date_of_registration',),
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.DateTimeField(verbose_name='Departure')),
                ('arrival', models.DateTimeField(verbose_name='Arrival')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
                ('destination_city', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='destination',
                    to='cities_light.City',
                    verbose_name='To')),
                ('origin_city', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='origin',
                    to='cities_light.City',
                    verbose_name='From')),
                ('scientific_mission', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='scientific_mission.ScientificMission')),
            ],
            options={
                'ordering': ('scientific_mission', 'order'),
            },
        ),
    ]
