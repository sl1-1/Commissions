# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0021_auto_20150704_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Submitted'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Details Submitted'),
        ),
    ]
