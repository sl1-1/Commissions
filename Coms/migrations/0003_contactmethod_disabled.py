# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0002_auto_20150627_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmethod',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
