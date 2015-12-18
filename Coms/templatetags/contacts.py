from django import template

import json

from Coms.models import ContactMethod

register = template.Library()


@register.inclusion_tag('templatetags/contact.html')
def render_contacts(contacts):
    primary = None
    additional = []

    for contact in json.loads(contacts):
        site = ContactMethod.objects.get(pk=contact['site_id'])
        contact.pop('site_id', None)
        contact['profile'] = site.profile(**contact)
        contact['message'] = site.message(**contact)
        if contact['primary']:
            primary = contact
        else:
            additional.append(contact)

    return {'primary': primary, 'contacts': additional}
