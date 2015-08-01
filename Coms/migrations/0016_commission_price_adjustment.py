# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0015_auto_20150701_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='price_adjustment',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
    ]
