# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0012_auto_20150630_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='accepted',
            field=models.IntegerField(default=0, choices=[(0, 'Waiting'), (1, 'Accepted'), (2, 'Rejected')]),
        ),
        migrations.AddField(
            model_name='commission',
            name='paid',
            field=models.BooleanField(default=0, choices=[(0, 'Not Yet Requested'), (1, 'Invoiced'), (2, 'Paid'), (3, 'Refunded')]),
        ),
        migrations.AddField(
            model_name='detail',
            name='Paypal',
            field=models.EmailField(max_length=254, default='Email@address.com'),
            preserve_default=False,
        ),
    ]
