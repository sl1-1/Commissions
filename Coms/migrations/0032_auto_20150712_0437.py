# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0031_auto_20150711_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comfile',
            name='comdetails',
        ),
        migrations.DeleteModel(
            name='ComFile',
        ),
    ]
