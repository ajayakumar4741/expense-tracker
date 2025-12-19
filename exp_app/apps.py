from django.apps import AppConfig


class ExpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exp_app'
    
    def ready(self):
        import exp_app.signals
