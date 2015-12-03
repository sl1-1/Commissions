# from django.db import models
from django.core.urlresolvers import reverse

import Coms.models as comsmodels


# Create your models here.

class AdminQueue(comsmodels.Queue):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('Admin:Queue:ShowQueue', args=[self.id])


class AdminCommission(comsmodels.Commission):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('Admin:Queue:ShowQueue', args=[self.id])


class AdminContactMethod(comsmodels.ContactMethod):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('Admin:Contact:Modify', args=[self.id])


class AdminType(comsmodels.Type):
    class Meta:
        proxy = True
        verbose_name = "Commission Types"

    def get_absolute_url(self):
        return reverse('Admin:Type:Modify', args=[self.id])


class AdminSize(comsmodels.Size):
    class Meta:
        proxy = True
        verbose_name = "Commission Sizes"

    def get_absolute_url(self):
        return reverse('Admin:Size:Modify', args=[self.id])


class AdminExtra(comsmodels.Extra):
    class Meta:
        proxy = True
        verbose_name = "Commission Extras"

    def get_absolute_url(self):
        return reverse('Admin:Extra:Modify', args=[self.id])

