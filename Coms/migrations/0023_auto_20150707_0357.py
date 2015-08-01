# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0022_auto_20150706_0340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='user',
            new_name='username',
        ),
    ]
