# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0005_auto_20160319_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='details_date',
            field=models.DateTimeField(blank=True, verbose_name=b'Details Submitted'),
        ),
    ]