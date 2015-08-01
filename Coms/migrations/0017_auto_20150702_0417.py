# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0016_commission_price_adjustment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='Contacts',
            field=models.ManyToManyField(to='Coms.Contact', blank=True),
        ),
    ]
