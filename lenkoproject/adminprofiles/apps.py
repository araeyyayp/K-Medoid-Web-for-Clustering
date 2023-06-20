from django.apps import AppConfig


class AdminprofilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminprofiles'

    def ready(self):
    	import adminprofiles.signals