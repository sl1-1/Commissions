# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0013_auto_20151223_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='commissionfiles',
            name='filename',
            field=models.CharField(default=' ', max_length=1000),
            preserve_default=False,
        ),
    ]
