# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0011_commissionfiles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commissionfiles',
            old_name='upload',
            new_name='type',
        ),
    ]
