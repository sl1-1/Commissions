# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0006_auto_20150627_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='Primary_Contact',
            field=models.ForeignKey(to='Coms.Contact', default=None),
        ),
    ]
