# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0017_remove_commissionfiles_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commissionfiles',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
