# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0011_auto_20150629_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='Contacts',
            field=models.ManyToManyField(blank=True, null=True, to='Coms.Contact'),
        ),
    ]
