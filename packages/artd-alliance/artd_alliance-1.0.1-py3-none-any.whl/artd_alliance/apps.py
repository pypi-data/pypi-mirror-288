from django.apps import AppConfig

class ArtdAllianceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artd_alliance'

    def ready(self):
        from artd_alliance import signals