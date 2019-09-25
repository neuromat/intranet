# Generated by Django 2.2.5 on 2019-09-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dissemination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Date')),
                ('link', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('type_of_media', models.CharField(
                    blank=True,
                    choices=[('i', 'Internal'), ('e', 'External')],
                    max_length=1,
                    verbose_name='Type of media')),
            ],
            options={
                'ordering': ('-date', 'title'),
            },
        ),
        migrations.CreateModel(
            name='ExternalMediaOutlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'External media outlet',
                'verbose_name_plural': 'External media outlets',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='InternalMediaOutlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Internal media outlet',
                'verbose_name_plural': 'Internal media outlets',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='External',
            fields=[
                ('dissemination_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='dissemination.Dissemination')),
            ],
            options={
                'verbose_name': 'External',
                'verbose_name_plural': 'External',
            },
            bases=('dissemination.dissemination',),
        ),
        migrations.CreateModel(
            name='Internal',
            fields=[
                ('dissemination_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='dissemination.Dissemination')),
            ],
            options={
                'verbose_name': 'Internal',
                'verbose_name_plural': 'Internal',
            },
            bases=('dissemination.dissemination',),
        ),
        migrations.AddField(
            model_name='dissemination',
            name='topic',
            field=models.ManyToManyField(blank=True, to='dissemination.Topic', verbose_name='Topic'),
        ),
    ]
