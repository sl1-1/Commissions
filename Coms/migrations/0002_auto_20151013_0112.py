# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='end',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
