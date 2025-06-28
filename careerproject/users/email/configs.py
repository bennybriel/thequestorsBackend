# email/config.py
from django.conf import settings

def get_email_config():
    """
    Returns the email configuration from Django settings
    """
    return {
        'API_URL': settings.EMAIL_TEMPLATES_URL,
        'SENDER_EMAIL': settings.EMAIL_SENDER,
        'API_TOKEN': settings.EMAIL_TOKEN,
        'TEMPLATE_KEY':settings.EMAIL_TEMPLATES_KEY,
        'TEMPLATE_KEY_RESET':settings.TEMPLATE_KEY_RESET,
        'TEMPLATES': getattr(settings, 'EMAIL_TEMPLATES', {})
    }