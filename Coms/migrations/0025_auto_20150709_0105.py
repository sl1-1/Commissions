# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0024_commission_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Generated at')),
                ('commission', models.ForeignKey(to='Coms.Commission', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='queue',
            name='token',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='queue',
            name='token_expire',
            field=models.IntegerField(default=15),
        ),
        migrations.AddField(
            model_name='ticket',
            name='queue',
            field=models.ForeignKey(to='Coms.Queue'),
        ),
    ]
