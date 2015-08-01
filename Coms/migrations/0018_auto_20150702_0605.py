# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0017_auto_20150702_0417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='Date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='commission',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='commission',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Character_cost',
            new_name='character_cost',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Extras',
            new_name='extras',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Max_characters',
            new_name='max_characters',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Max_commissions_in_queue',
            new_name='max_commissions_in_queue',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Max_commissions_per_person',
            new_name='max_commissions_per_person',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Sizes',
            new_name='sizes',
        ),
        migrations.RenameField(
            model_name='queue',
            old_name='Types',
            new_name='type',
        ),
    ]
