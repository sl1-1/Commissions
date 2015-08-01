# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0010_auto_20150628_0524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmethod',
            old_name='url',
            new_name='message_url',
        ),
        migrations.AddField(
            model_name='contactmethod',
            name='profile_url',
            field=models.URLField(blank=True),
        ),
    ]
