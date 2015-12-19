# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Coms', '0002_admincommission_admincontactmethod_adminextra_adminqueue_adminsize_admintype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='price_adjustment',
        ),
        migrations.AddField(
            model_name='commission',
            name='contacts',
            field=models.ManyToManyField(default=None, to='Coms.Contact', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='commission',
            name='details',
            field=models.TextField(default=None, max_length=10000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='commission',
            name='details_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'Details Submitted', blank=True),
        ),
        migrations.AddField(
            model_name='commission',
            name='extras',
            field=models.ManyToManyField(to='Coms.Extra', blank=True),
        ),
        migrations.AddField(
            model_name='commission',
            name='number_of_Characters',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='commission',
            name='paypal',
            field=models.EmailField(default=None, max_length=254, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='commission',
            name='size',
            field=models.ForeignKey(default=None, blank=True, to='Coms.Size', null=True),
        ),
        migrations.AddField(
            model_name='commission',
            name='type',
            field=models.ForeignKey(default=None, blank=True, to='Coms.Type', null=True),
        ),
    ]
