# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0015_auto_20151223_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='commissionfiles',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commissionfiles',
            name='user_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
