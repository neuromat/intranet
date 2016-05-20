# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0004_email_max_length_was_increased'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('funding', models.BooleanField(choices=[(True, b'Yes'), (False, b'No')], max_length=3,
                                                verbose_name='Financially supported?')),
                ('funding_agency', models.CharField(blank=True, max_length=255, verbose_name='Funding agency')),
                ('url', models.URLField(blank=True, help_text=b'URL to funding information.', max_length=255,
                                        null=True, verbose_name='URL')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('abstract', models.TextField(verbose_name='Abstract')),
                ('advisee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person',
                                              verbose_name='Advisee')),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='advisor_academic_work', to='person.Person',
                                              verbose_name='Advisor')),
                ('co_advisor', models.ManyToManyField(blank=True, related_name='co_advisor_academic_work',
                                                      to='person.Person', verbose_name='Co-Advisor')),
            ],
            options={
                'ordering': ('-start_date',),
                'verbose_name': 'Academic Work',
                'verbose_name_plural': 'Academic Works',
            },
        ),
        migrations.CreateModel(
            name='Accepted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=b'', verbose_name='Attachment')),
                ('date', models.DateField(verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Accepted',
                'verbose_name_plural': 'Accepted',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(verbose_name='Order of author')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=b'', verbose_name='Attachment')),
                ('date', models.DateField(verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Draft',
                'verbose_name_plural': 'Draft',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('acronym', models.CharField(blank=True, max_length=50, null=True, verbose_name='Acronym')),
                ('volume', models.CharField(blank=True, max_length=255, null=True, verbose_name='Volume')),
                ('number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number')),
                ('start_date', models.DateField(verbose_name='Start date of the event')),
                ('end_date', models.DateField(verbose_name='End date of the event')),
                ('local', models.CharField(help_text=b'Where the conference was held, e.g., '
                                                     b'"Rio de Janeiro, RJ, Brazil".',
                                           max_length=255, verbose_name='Local')),
                ('publisher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                to='person.Institution', verbose_name='Publisher')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events (congress, conference, etc.)',
            },
        ),
        migrations.CreateModel(
            name='EventRISFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.Event')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Event name on the RIS file',
                'verbose_name_plural': 'Event name on the RIS file',
            },
        ),
        migrations.CreateModel(
            name='Periodical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('acronym', models.CharField(blank=True, max_length=50, null=True, verbose_name='Acronym')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Periodical',
                'verbose_name_plural': 'Periodicals',
            },
        ),
        migrations.CreateModel(
            name='PeriodicalRISFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('periodical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to='research.Periodical')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Periodical name on the RIS file',
                'verbose_name_plural': 'Periodical name on the RIS file',
            },
        ),
        migrations.CreateModel(
            name='Published',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doi', models.CharField(blank=True, max_length=255, null=True, verbose_name='DOI')),
                ('start_page', models.IntegerField(blank=True, null=True, verbose_name='Start page')),
                ('end_page', models.IntegerField(blank=True, null=True, verbose_name='End page')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=b'', verbose_name='Attachment')),
            ],
            options={
                'verbose_name': 'Published',
                'verbose_name_plural': 'Published',
            },
        ),
        migrations.CreateModel(
            name='ResearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(choices=[(b's', 'Scientific'), (b'd', 'Dissemination'),
                                                   (b't', 'Technology transfer')], max_length=1, verbose_name='Team')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.URLField(blank=True, max_length=255, null=True, verbose_name='URL')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
                ('research_result_type', models.CharField(blank=True, choices=[(b'a', 'Article'), (b'b', 'Book')],
                                                          max_length=1, verbose_name='Type')),
                ('ris_file_authors', models.CharField(blank=True, max_length=255, null=True,
                                                      verbose_name='RIS file authors')),
            ],
        ),
        migrations.CreateModel(
            name='Submitted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=b'', verbose_name='Attachment')),
                ('date', models.DateField(verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Submitted',
                'verbose_name_plural': 'Submitted',
            },
        ),
        migrations.CreateModel(
            name='TypeAcademicWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Type of Academic Work',
                'verbose_name_plural': 'Types of Academic Work',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('researchresult_ptr', models.OneToOneField(auto_created=True,
                                                            on_delete=django.db.models.deletion.CASCADE,
                                                            parent_link=True, primary_key=True, serialize=False,
                                                            to='research.ResearchResult')),
                ('type', models.CharField(blank=True, choices=[(b'p', 'Periodical (Journal or magazine)'),
                                                               (b'e', 'Event (Conference, congress, meeting, etc)')],
                                          max_length=1, null=True, verbose_name='Where?')),
                ('status', models.CharField(max_length=50, verbose_name='Status')),
                ('hide', models.BooleanField(default=False, verbose_name='Hide this paper in the report')),
                ('event', models.ForeignKey(blank=True, help_text=b'Name of the conference, congress, meeting or '
                                                                  b'symposium',
                                            null=True, on_delete=django.db.models.deletion.CASCADE, to='research.Event',
                                            verbose_name='Event')),
                ('periodical', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 to='research.Periodical', verbose_name='Periodical')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
            bases=('research.researchresult',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('researchresult_ptr', models.OneToOneField(auto_created=True,
                                                            on_delete=django.db.models.deletion.CASCADE,
                                                            parent_link=True, primary_key=True, serialize=False,
                                                            to='research.ResearchResult')),
                ('type', models.CharField(choices=[(b'b', 'Book'), (b'c', 'Chapter')], max_length=1,
                                          verbose_name='Type')),
                ('isbn', models.CharField(blank=True, max_length=30, null=True, verbose_name='ISBN')),
                ('volume', models.CharField(blank=True, max_length=255, null=True, verbose_name='Volume/Number')),
                ('serie', models.CharField(blank=True, max_length=255, null=True, verbose_name='Serie')),
                ('edition', models.CharField(blank=True, max_length=255, null=True, verbose_name='Edition')),
                ('doi', models.CharField(blank=True, max_length=255, null=True, verbose_name='DOI')),
                ('date', models.DateField(help_text=b'Date the book was published.', verbose_name='Date')),
                ('chapter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Chapter')),
                ('start_page', models.IntegerField(blank=True, null=True, verbose_name='Start page')),
                ('end_page', models.IntegerField(blank=True, null=True, verbose_name='End page')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Institution',
                                                verbose_name='Publisher')),
            ],
            options={
                'verbose_name': 'Book and chapter',
                'verbose_name_plural': 'Books and chapters',
            },
            bases=('research.researchresult',),
        ),
        migrations.CreateModel(
            name='PublishedInPeriodical',
            fields=[
                ('published_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                       parent_link=True, primary_key=True, serialize=False,
                                                       to='research.Published')),
                ('volume', models.CharField(blank=True, max_length=255, null=True, verbose_name='Volume')),
                ('number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number')),
                ('date', models.DateField(verbose_name='Date')),
            ],
            bases=('research.published',),
        ),
        migrations.AddField(
            model_name='researchresult',
            name='person',
            field=models.ManyToManyField(through='research.Author', to='person.Person'),
        ),
        migrations.AddField(
            model_name='author',
            name='research_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.ResearchResult'),
        ),
        migrations.AddField(
            model_name='academicwork',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.TypeAcademicWork',
                                    verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='submitted',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.Article'),
        ),
        migrations.AddField(
            model_name='published',
            name='article',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='research.Article',
                                       verbose_name='Article'),
        ),
        migrations.AddField(
            model_name='draft',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.Article'),
        ),
        migrations.AddField(
            model_name='accepted',
            name='article',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='research.Article'),
        ),
    ]
