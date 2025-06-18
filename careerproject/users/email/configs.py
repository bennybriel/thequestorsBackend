# email/config.py
from django.conf import settings

def get_email_config():
    """
    Returns the email configuration from Django settings
    """
    return {
        'API_URL': settings.EMAIL_URL,
        'SENDER_EMAIL': settings.EMAIL_SENDER,
        'API_TOKEN': settings.EMAIL_TOKEN,
        'TEMPLATES': getattr(settings, 'EMAIL_TEMPLATES', {})
    }