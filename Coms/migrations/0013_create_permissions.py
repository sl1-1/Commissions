import Coms.models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations


def create_groups(apps, schema_editor):
    new_group = Group.objects.get_or_create(name="Commissioners")[0]
    add_commission = Permission.objects.get(id=30)
    new_group.permissions.add(add_commission)

    new_group.permissions.add(add_commission)
    view_commission = Permission.objects.get(id=31)
    new_group.permissions.add(view_commission)
    change_commission = Permission.objects.get(id=32)
    new_group.permissions.add(change_commission)


class Migration(migrations.Migration):
    dependencies = [
        ('Coms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
