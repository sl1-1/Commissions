# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0006_auto_20151217_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='commission',
            name='details_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 18, 4, 36, 3, 594440, tzinfo=utc), verbose_name=b'Details Submitted', auto_now=True),
            preserve_default=False,
        ),
    ]
