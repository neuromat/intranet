# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
        ('person', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('justification', models.TextField(verbose_name='Justification')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Order date')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('type_of_order', models.CharField(blank=True, max_length=1, verbose_name='Type of order', choices=[('e', 'Scientific event'), ('h', 'Equipment / Supplies / Miscellaneous'), ('s', 'Service'), ('t', 'Ticket'), ('d', 'Daily stipend'), ('r', 'Reimbursement')])),
                ('status', models.CharField(default='o', max_length=1, blank=True, choices=[('o', 'Open'), ('p', 'Pending'), ('c', 'Canceled'), ('a', 'Approved'), ('d', 'Denied'), ('f', 'Finished')])),
                ('protocol', models.IntegerField(null=True, verbose_name='Protocol', blank=True)),
            ],
            options={
                'ordering': ('-date_modified',),
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HardwareSoftware',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.Order')),
                ('type', models.TextField(max_length=500, verbose_name='Description')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('url', models.URLField(help_text='Link to the product details. You may suggest an URL address of the manufacturer of the product or any store that sells this product.', max_length=255, null=True, verbose_name='URL', blank=True)),
                ('origin', models.CharField(max_length=1, null=True, verbose_name='Origin', blank=True)),
                ('category', models.CharField(max_length=1, null=True, verbose_name='Category', blank=True)),
                ('institution', models.ForeignKey(verbose_name='Institution', blank=True, to='person.Institution', null=True)),
            ],
            options={
                'verbose_name': 'Equipment / Supplies / Miscellaneous',
                'verbose_name_plural': 'Equipment / Supplies / Miscellaneous',
            },
            bases=('order.order',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.Order')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('url', models.URLField(max_length=255, null=True, verbose_name='URL', blank=True)),
                ('value', models.CharField(max_length=15, null=True, verbose_name='Value', blank=True)),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('invitation', models.FileField(upload_to=b'', null=True, verbose_name='Invitation', blank=True)),
            ],
            options={
                'verbose_name': 'Scientific event',
                'verbose_name_plural': 'Scientific events',
            },
            bases=('order.order',),
        ),
        migrations.CreateModel(
            name='DailyStipend',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.Order')),
                ('origin', models.CharField(max_length=200, verbose_name='Origin')),
                ('destination', models.CharField(max_length=200, verbose_name='Destination')),
                ('departure', models.DateTimeField(verbose_name='Departure')),
                ('arrival', models.DateTimeField(verbose_name='Arrival')),
            ],
            options={
                'verbose_name': 'Daily stipend',
                'verbose_name_plural': 'Daily stipends',
            },
            bases=('order.order',),
        ),
        migrations.CreateModel(
            name='Reimbursement',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.Order')),
                ('why', models.TextField(max_length=500, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Reimbursement',
                'verbose_name_plural': 'Reimbursements',
            },
            bases=('order.order',),
        ),
        migrations.CreateModel(
            name='ScientificMission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mission', models.CharField(max_length=255, null=True, verbose_name='Scientific Mission', blank=True)),
            ],
            options={
                'ordering': ('mission',),
                'verbose_name': 'Scientific Mission',
                'verbose_name_plural': 'Scientific Missions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.Order')),
                ('type', models.TextField(max_length=500, verbose_name='Description')),
                ('origin', models.CharField(max_length=1, null=True, verbose_name='Origin', blank=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=('order.order',),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.Order')),
                ('origin', models.CharField(max_length=200, verbose_name='Origin')),
                ('destination', models.CharField(max_length=200, verbose_name='Destination')),
                ('outbound_date', models.DateField(verbose_name='Outbound Date')),
                ('outbound_date_preference', models.CharField(max_length=10, null=True, verbose_name='Outbound Preferred time', blank=True)),
                ('inbound_date', models.DateField(null=True, verbose_name='Inbound Date', blank=True)),
                ('inbound_date_preference', models.CharField(max_length=10, null=True, verbose_name='Inbound Preferred time', blank=True)),
                ('type', models.NullBooleanField(verbose_name='Type of Trip')),
                ('type_transportation', models.NullBooleanField(verbose_name='Type of transportation')),
                ('note', models.CharField(max_length=200, null=True, verbose_name='Note', blank=True)),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
            bases=('order.order',),
        ),
        migrations.AddField(
            model_name='order',
            name='requester',
            field=models.ForeignKey(verbose_name='NeuroMat member', to='person.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dailystipend',
            name='mission',
            field=models.ForeignKey(verbose_name='Mission', blank=True, to='order.ScientificMission', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dailystipend',
            name='project_activity',
            field=models.ForeignKey(verbose_name='Project activity', blank=True, to='activity.ProjectActivities', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dailystipend',
            name='receiver',
            field=models.ForeignKey(verbose_name='Who will receive?', blank=True, to='person.Person', null=True),
            preserve_default=True,
        ),
    ]
