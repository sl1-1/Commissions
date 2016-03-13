from django import template
from django import forms

import Coms.models as models

register = template.Library()


class CommissionFileUpload(forms.ModelForm):
    class Meta(object):
        model = models.CommissionFiles
        fields = ('note', 'img')


@register.inclusion_tag('templatetags/files.html', takes_context=True)
def render_files(context, commission):
    files = commission.commissionfiles_set.all().order_by('-date')
    fileform = CommissionFileUpload()

    return {'files': files, 'fileform': fileform, 'commission': commission, 'request': context['request']}
