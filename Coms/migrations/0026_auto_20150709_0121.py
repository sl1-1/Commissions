# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0025_auto_20150709_0105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queue',
            old_name='token_expire',
            new_name='ticket_expire',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='token',
            new_name='use_ticket',
        ),
    ]
