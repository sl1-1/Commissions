# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserControl', '0002_character_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='friendlyid',
            field=models.CharField(max_length=110, blank=True),
        ),
    ]
