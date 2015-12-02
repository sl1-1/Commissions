from django.db import models
from django.contrib.auth.models import User
import uuid
import os.path as path
from django.core.urlresolvers import reverse


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    send_email = models.BooleanField(default=True)


