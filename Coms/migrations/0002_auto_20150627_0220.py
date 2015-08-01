# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmethod',
            name='description',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='contactmethod',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
