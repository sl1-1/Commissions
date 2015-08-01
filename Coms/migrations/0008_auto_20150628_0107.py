# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0007_auto_20150628_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='Primary_Contact',
            field=models.ForeignKey(blank=True, to='Coms.Contact'),
        ),
    ]
