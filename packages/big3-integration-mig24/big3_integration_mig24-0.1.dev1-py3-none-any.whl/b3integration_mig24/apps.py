from django.apps import AppConfig


class B3IntegrationMig24Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b3integration_mig24'
    is_integration = True
