# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0014_auto_20150701_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='accepted',
        ),
        migrations.AddField(
            model_name='commission',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting'), (1, 'Accepted'), (2, 'Rejected'), (3, 'Work In Progress'), (4, 'Competed')], default=0),
        ),
    ]
