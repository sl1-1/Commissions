# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('file_name', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('User', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=254)),
                ('Date', models.DateTimeField(verbose_name='date entered', auto_now_add=True)),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Contact Method',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('Number_of_Characters', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('Details', models.TextField(max_length=2000)),
                ('Date', models.DateTimeField(verbose_name='date entered', auto_now_add=True)),
                ('Contact_Method', models.ForeignKey(to='Coms.ContactMethod')),
            ],
            options={
                'verbose_name': 'Commission Detail',
            },
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, default=0.0)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
                'verbose_name': 'Commission Extra',
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('Name', models.CharField(max_length=200)),
                ('Date', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('Max_characters', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('Character_cost', models.DecimalField(decimal_places=2, max_digits=5, default=0.0)),
                ('Max_commissions_in_queue', models.IntegerField(default=1)),
                ('Max_commissions_per_person', models.IntegerField(default=1)),
                ('Extras', models.ManyToManyField(blank=True, to='Coms.Extra')),
            ],
            options={
                'verbose_name': 'Commission Queue',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, default=0.0)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
                'verbose_name': 'Commission Size',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, default=0.0)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
                'verbose_name': 'Commission Type',
            },
        ),
        migrations.AddField(
            model_name='queue',
            name='Sizes',
            field=models.ManyToManyField(to='Coms.Size'),
        ),
        migrations.AddField(
            model_name='queue',
            name='Types',
            field=models.ManyToManyField(to='Coms.Type'),
        ),
        migrations.AddField(
            model_name='detail',
            name='Extras',
            field=models.ManyToManyField(blank=True, to='Coms.Extra'),
        ),
        migrations.AddField(
            model_name='detail',
            name='Size',
            field=models.ForeignKey(to='Coms.Size'),
        ),
        migrations.AddField(
            model_name='detail',
            name='Type',
            field=models.ForeignKey(to='Coms.Type'),
        ),
        migrations.AddField(
            model_name='detail',
            name='com',
            field=models.ForeignKey(to='Coms.Commission'),
        ),
        migrations.AddField(
            model_name='commission',
            name='queue',
            field=models.ForeignKey(to='Coms.Queue'),
        ),
        migrations.AddField(
            model_name='comfile',
            name='comdetails',
            field=models.ForeignKey(to='Coms.Detail'),
        ),
    ]
