# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0003_auto_20151214_0317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='contacts',
        ),
        migrations.AddField(
            model_name='commission',
            name='contacts',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
