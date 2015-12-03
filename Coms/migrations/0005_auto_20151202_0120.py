# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0004_auto_20151202_0117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extra',
            old_name='extra_char_price',
            new_name='extra_character_price',
        ),
        migrations.RenameField(
            model_name='size',
            old_name='extra_char_price',
            new_name='extra_character_price',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='extra_char_price',
            new_name='extra_character_price',
        ),
    ]
