from django.db import models
from django.core.urlresolvers import reverse

import Coms.models as comsmodels


# Create your models here.

class AdminQueue(comsmodels.Queue):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('Admin:Queue:ShowQueue', args=[self.id])


class AdminContactMethod(comsmodels.ContactMethod):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('Admin:Contact:Show')
