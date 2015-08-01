# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0004_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='data',
            new_name='username',
        ),
        migrations.AddField(
            model_name='contact',
            name='type',
            field=models.ForeignKey(default=1, to='Coms.ContactMethod'),
            preserve_default=False,
        ),
    ]
