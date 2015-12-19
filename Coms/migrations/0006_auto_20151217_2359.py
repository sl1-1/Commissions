# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0005_auto_20151215_2354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='details',
            new_name='description',
        ),
    ]
