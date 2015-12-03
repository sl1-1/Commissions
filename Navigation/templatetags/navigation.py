from django import template

from Navigation.signals import render_navbar, render_navbar_admin
from collections import defaultdict

register = template.Library()


@register.inclusion_tag('Navigation/navbar.html', takes_context=True)
def navbar(context):
    urls = defaultdict(list)
    render_navbar.send(sender=None, urls=urls)
    if context['user'].is_staff:
        render_navbar_admin.send(sender=None, urls=urls)
    print(urls)
    context['urls'] = dict(urls)
    print(context)
    return context
