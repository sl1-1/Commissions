# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0019_auto_20150702_0609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detail',
            old_name='Contacts',
            new_name='contacts',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Details',
            new_name='details',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Extras',
            new_name='extras',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Number_of_Characters',
            new_name='number_of_Characters',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Paypal',
            new_name='paypal',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Primary_Contact',
            new_name='primary_contact',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Size',
            new_name='size',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='Type',
            new_name='type',
        ),
    ]
