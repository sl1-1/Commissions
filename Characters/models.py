import uuid

import os.path as path
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.


def ref_name(instance, filename):
    user = instance.user.id
    name = instance.name
    return path.join(str(user), 'ref', name, str(uuid.uuid4()), filename)


class Character(models.Model):
    def __unicode__(self):
        return self.friendly

    def __str__(self):
        return self.friendly

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    img = models.ImageField(upload_to=ref_name)
    date = models.DateTimeField(auto_now=True)
    friendlyid = models.CharField(max_length=110)

    def get_absolute_url(self):
        return reverse('Characters:Character', args=[self.id])

    def create_friendly(self):
        count = Character.objects.filter(user=self.user).filter(name=self.name).count()
        return "{0}~{1}".format(self.name, count)

    def save(self, *args, **kwargs):
        self.friendlyid = self.create_friendly()
        super(Character, self).save(*args, **kwargs)
