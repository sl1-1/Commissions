# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Character = apps.get_model("UserControl", "Character")
    db_alias = schema_editor.connection.alias
    for object in Character.objects.all():
        count = Character.objects.filter(user=object.user).filter(name=object.name).count()
        object.friendlyid = "{}~{}".format(object.name, count)
        object.save()

class Migration(migrations.Migration):

    dependencies = [
        ('UserControl', '0004_remove_character_friendlyid'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='friendlyid',
            field=models.CharField(default='FIXME', max_length=110),
            preserve_default=False,
        ),
        migrations.RunPython(
            forwards_func,
        ),

    ]
