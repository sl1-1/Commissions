# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0028_ticket_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='commission',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='queue',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='ticket_expire',
            new_name='expire',
        ),
        migrations.RemoveField(
            model_name='queue',
            name='use_ticket',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
