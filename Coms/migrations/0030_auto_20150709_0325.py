# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0029_auto_20150709_0238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='email',
        ),
        migrations.RemoveField(
            model_name='commission',
            name='username',
        ),
    ]
