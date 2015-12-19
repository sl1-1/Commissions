# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0007_auto_20151218_0436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='number_of_Characters',
            new_name='number_of_characters',
        ),
    ]
