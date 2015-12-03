# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0002_auto_20151013_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
