# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0013_auto_20150701_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='paid',
            field=models.IntegerField(choices=[(0, 'Not Yet Requested'), (1, 'Invoiced'), (2, 'Paid'), (3, 'Refunded')], default=0),
        ),
    ]
