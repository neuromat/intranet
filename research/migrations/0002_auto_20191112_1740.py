# Generated by Django 2.2.5 on 2019-11-12 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicwork',
            name='advisee',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='person.Person',
                verbose_name='Advisee'),
        ),
        migrations.AlterField(
            model_name='academicwork',
            name='advisor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='advisor_academic_work',
                to='person.Person',
                verbose_name='Advisor'),
        ),
        migrations.AlterField(
            model_name='academicwork',
            name='type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='research.TypeAcademicWork',
                verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='article',
            name='event',
            field=models.ForeignKey(
                blank=True,
                help_text='Name of the conference, congress, meeting or symposium',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='research.Event',
                verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='article',
            name='periodical',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='research.Periodical',
                verbose_name='Periodical'),
        ),
        migrations.AlterField(
            model_name='author',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='person.Person'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='person.Institution',
                verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='event',
            name='publisher',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='person.Institution',
                verbose_name='Publisher'),
        ),
    ]