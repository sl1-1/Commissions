# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0033_auto_20150714_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='queue',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
