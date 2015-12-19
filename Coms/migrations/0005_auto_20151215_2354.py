# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0004_auto_20151215_0531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='site',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='com',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='extras',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='size',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='type',
        ),
        migrations.DeleteModel(
            name='AdminCommission',
        ),
        migrations.DeleteModel(
            name='AdminContactMethod',
        ),
        migrations.DeleteModel(
            name='AdminExtra',
        ),
        migrations.DeleteModel(
            name='AdminQueue',
        ),
        migrations.DeleteModel(
            name='AdminSize',
        ),
        migrations.DeleteModel(
            name='AdminType',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Detail',
        ),
    ]
