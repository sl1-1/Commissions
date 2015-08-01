# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0027_auto_20150709_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ip',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
    ]
