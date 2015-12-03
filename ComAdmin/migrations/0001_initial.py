# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCommission',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('Coms.commission',),
        ),
        migrations.CreateModel(
            name='AdminContactMethod',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('Coms.contactmethod',),
        ),
        migrations.CreateModel(
            name='AdminExtra',
            fields=[
            ],
            options={
                'verbose_name': 'Commission Extras',
                'proxy': True,
            },
            bases=('Coms.extra',),
        ),
        migrations.CreateModel(
            name='AdminQueue',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('Coms.queue',),
        ),
        migrations.CreateModel(
            name='AdminSize',
            fields=[
            ],
            options={
                'verbose_name': 'Commission Sizes',
                'proxy': True,
            },
            bases=('Coms.size',),
        ),
        migrations.CreateModel(
            name='AdminType',
            fields=[
            ],
            options={
                'verbose_name': 'Commission Types',
                'proxy': True,
            },
            bases=('Coms.type',),
        ),
    ]
