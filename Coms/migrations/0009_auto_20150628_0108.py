# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0008_auto_20150628_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='Primary_Contact',
            field=models.ForeignKey(blank=True, null=True, to='Coms.Contact'),
        ),
    ]
