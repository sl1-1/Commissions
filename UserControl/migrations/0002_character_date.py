# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('UserControl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 12, 4, 24, 43, 845402, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
