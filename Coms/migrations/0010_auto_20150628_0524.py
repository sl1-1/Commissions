# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0009_auto_20150628_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='Contacts',
            field=models.ManyToManyField(to='Coms.Contact'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='Primary_Contact',
            field=models.ForeignKey(blank=True, related_name='detail_pc', to='Coms.Contact', null=True),
        ),
    ]
