# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0003_queue_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='extra_char_price',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='size',
            name='extra_char_price',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='type',
            name='extra_char_price',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
    ]
