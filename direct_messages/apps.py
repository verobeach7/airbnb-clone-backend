from django.apps import AppConfig


class DirectMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "direct_messages"
    # App 이름 변경은 여기에서
    verbose_name = "Direct Messages"
