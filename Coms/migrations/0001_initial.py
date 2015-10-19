# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Submitted')),
                ('locked', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Waiting'), (1, b'Sketched'), (2, b'Lined'), (3, b'Coloured'), (4, b'Finished'), (5, b'Canceled'), (6, b'Please Revise'), (7, b'Rejected')])),
                ('paid', models.IntegerField(default=0, choices=[(0, b'Not Yet Requested'), (1, b'Invoiced'), (2, b'Paid'), (3, b'Refunded')])),
                ('price_adjustment', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('primary', models.BooleanField(default=False)),
                ('commission', models.ForeignKey(to='Coms.Commission')),
            ],
        ),
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('message_url', models.URLField(blank=True)),
                ('profile_url', models.URLField(blank=True)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Contact Method',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('number_of_Characters', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('details', models.TextField(max_length=10000)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Details Submitted')),
                ('paypal', models.EmailField(max_length=254)),
                ('com', models.ForeignKey(to='Coms.Commission')),
                ('contacts', models.ManyToManyField(to='Coms.Contact', blank=True)),
            ],
            options={
                'verbose_name': 'Commission Detail',
            },
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Commission Extra',
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('max_characters', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('character_cost', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('max_commissions_in_queue', models.IntegerField(default=1)),
                ('max_commissions_per_person', models.IntegerField(default=1)),
                ('expire', models.IntegerField(default=15)),
                ('closed', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('extras', models.ManyToManyField(to='Coms.Extra', blank=True)),
            ],
            options={
                'verbose_name': 'Commission Queue',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Commission Size',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(default=0.0, max_digits=5, decimal_places=2)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Commission Type',
            },
        ),
        migrations.AddField(
            model_name='queue',
            name='sizes',
            field=models.ManyToManyField(to='Coms.Size'),
        ),
        migrations.AddField(
            model_name='queue',
            name='types',
            field=models.ManyToManyField(to='Coms.Type'),
        ),
        migrations.AddField(
            model_name='detail',
            name='extras',
            field=models.ManyToManyField(to='Coms.Extra', blank=True),
        ),
        migrations.AddField(
            model_name='detail',
            name='primary_contact',
            field=models.ForeignKey(related_name='detail_pc', blank=True, to='Coms.Contact', null=True),
        ),
        migrations.AddField(
            model_name='detail',
            name='size',
            field=models.ForeignKey(to='Coms.Size'),
        ),
        migrations.AddField(
            model_name='detail',
            name='type',
            field=models.ForeignKey(to='Coms.Type'),
        ),
        migrations.AddField(
            model_name='contact',
            name='site',
            field=models.ForeignKey(to='Coms.ContactMethod'),
        ),
        migrations.AddField(
            model_name='commission',
            name='queue',
            field=models.ForeignKey(to='Coms.Queue'),
        ),
        migrations.AddField(
            model_name='commission',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
