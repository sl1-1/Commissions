# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 05:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0002_auto_20160319_0418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commissionfiles',
            options={'default_permissions': ('add', 'view', 'change')},
        ),
        migrations.AlterModelOptions(
            name='queue',
            options={'default_permissions': ('view',)},
        ),
    ]
