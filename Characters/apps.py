from django.apps import AppConfig


class CharactersConfig(AppConfig):
    name = 'Characters'
    verbose_name = 'Characters'

    def ready(self):
        from hooks.templatehook import hook
        from views import detailhtml
        hook.register('detail_form', detailhtml)
