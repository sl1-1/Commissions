# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0008_auto_20151219_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='description',
            field=models.TextField(default=None, max_length=10000, blank=True),
        ),
        migrations.AlterField(
            model_name='commission',
            name='paypal',
            field=models.EmailField(default=None, max_length=254, blank=True),
        ),
    ]
