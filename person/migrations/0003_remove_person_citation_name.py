# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_citationname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='citation_name',
        ),
    ]
