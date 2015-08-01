# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0003_contactmethod_disabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, serialize=False)),
                ('data', models.CharField(max_length=100)),
                ('commission', models.ForeignKey(to='Coms.Commission')),
            ],
        ),
    ]
