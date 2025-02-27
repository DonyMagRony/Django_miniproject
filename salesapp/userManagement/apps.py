from django.apps import AppConfig

class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userManagement'

    def ready(self):
        import userManagement.signals  # Ensure signals are loaded
