# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0012_auto_20151223_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='commissionfiles',
            name='commission',
            field=models.ForeignKey(to='Coms.Commission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commissionfiles',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 23, 1, 15, 37, 721290, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
