# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0034_auto_20150719_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='end',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
