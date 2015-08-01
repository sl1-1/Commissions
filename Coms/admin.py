from django.contrib import admin

import Coms.models as models

# Register your models here.
admin.site.register(models.Queue)
admin.site.register(models.Commission)
admin.site.register(models.Detail)
admin.site.register(models.Contact)
admin.site.register(models.ContactMethod)
