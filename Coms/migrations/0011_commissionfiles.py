# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid
import Coms.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Coms', '0010_auto_20151219_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommissionFiles',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('upload', models.IntegerField(choices=[(1, b'Sketch'), (2, b'Lines'), (3, b'Colours'), (4, b'Finished')])),
                ('note', models.TextField(default=b'', max_length=1000, blank=True)),
                ('img', models.ImageField(upload_to=Coms.models.file_name)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
