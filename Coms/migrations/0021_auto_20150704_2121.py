# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0020_auto_20150702_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='detail',
            name='details',
            field=models.TextField(max_length=10000),
        ),
    ]
