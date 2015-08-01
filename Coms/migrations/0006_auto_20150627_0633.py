# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0005_auto_20150627_0316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='type',
            new_name='site',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='Contact_Method',
        ),
        migrations.AddField(
            model_name='detail',
            name='Primary_Contact',
            field=models.ForeignKey(to='Coms.Contact', default=0),
            preserve_default=False,
        ),
    ]
