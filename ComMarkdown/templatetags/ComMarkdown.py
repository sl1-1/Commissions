from django import template

from django.core.exceptions import ObjectDoesNotExist
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

import markdown

from UserControl import models as UserModels


class CharacterByID(Pattern):
    def handleMatch(self, m):
        try:
            character = UserModels.Character.objects.get(pk=m.group(3))
        except ObjectDoesNotExist:
            return m.group(2)
        el = etree.Element('button', {'class': 'btn btn-default character-popover', 'title': character.name,
                                      'id': str(character.id)})
        el.text = character.name
        return el


class CharacterByFriendly(Pattern):
    def __init__(self, pattern, config):
        super(CharacterByFriendly, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        print(self.config)
        try:
            character = UserModels.Character.objects.filter(user=self.config['user']).get(friendlyid=m.group(2))
        except ObjectDoesNotExist:
            try:
                character = UserModels.Character.objects.filter(user=self.config['user']).get(name=m.group(2))
            except ObjectDoesNotExist:
                return m.group(2)
        el = etree.Element('button', {'class': 'btn btn-default character-popover', 'title': character.name,
                                      'id': str(character.id)})
        el.text = character.name
        return el


class ComsMarkdown(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'user': ['', 'Commission User'],
            'commission': ['', 'Commission ID'],
            'detail': ['', 'Commission Detail ID']
        }
        super(ComsMarkdown, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['submission'] = CharacterByID(r'\(\!(.*?)\:([\w\-]*)\)')
        md.inlinePatterns['CharacterByFriendly'] = CharacterByFriendly(r'\(\Character:(.*?)\)', self.getConfigs())


# noinspection PyPep8Naming
def makeExtension(*args, **kwargs):
    return ComsMarkdown(*args, **kwargs)

register = template.Library()


@register.simple_tag(takes_context=True)
def com_markdown(context, value):
    request = context['request']
    user = request.user
    return markdown.markdown(value, extensions=[ComsMarkdown(user=user)])
