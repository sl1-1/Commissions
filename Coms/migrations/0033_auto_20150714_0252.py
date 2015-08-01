# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0032_auto_20150712_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Waiting'), (1, b'Sketched'), (2, b'Lined'), (3, b'Coloured'), (4, b'Finished'), (5, b'Canceled'), (6, b'Please Revise'), (7, b'Rejected')]),
        ),
    ]
