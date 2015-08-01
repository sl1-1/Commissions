# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0018_auto_20150702_0605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queue',
            old_name='type',
            new_name='types',
        ),
    ]
