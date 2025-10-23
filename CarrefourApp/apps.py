from django.apps import AppConfig


class CarrefourappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CarrefourApp'
    
    def ready(self):
        """Importer les signals lors du démarrage de l'application"""
        import CarrefourApp.signals

