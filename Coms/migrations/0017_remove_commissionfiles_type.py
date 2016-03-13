# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0016_auto_20160312_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commissionfiles',
            name='type',
        ),
    ]
