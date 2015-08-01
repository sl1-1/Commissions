from markdown.extensions import Extension

from markdown.inlinepatterns import Pattern
from markdown.util import etree


class Character(Pattern):
    def handleMatch(self, m):
        print('match')
        print(m.group(3))
        el = etree.Element('button', {'class': 'btn btn-default character-popover', 'title': m.group(2),
                                      'id': m.group(3)})
        el.text = "Character: {}".format(m.group(2))
        return el


class ComsMarkdown(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['submission'] = Character(r'\(\!(.*?)\:([\w\-]*)\)')


# noinspection PyPep8Naming
def makeExtension(*args, **kwargs):
    return ComsMarkdown(*args, **kwargs)
