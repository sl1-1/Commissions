# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0030_auto_20150709_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='size',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='type',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
