# email/validators.py
from django.core.exceptions import ImproperlyConfigured

def validate_email_config():
    """Validate that all required email settings are configured"""
    from django.conf import settings
    
    required_settings = ['API_URL', 'SENDER_EMAIL', 'API_TOKEN']
    for setting in required_settings:
        if not hasattr(settings, setting) or not getattr(settings, setting):
            raise ImproperlyConfigured(f"Missing required email setting: {setting}")
    
    if not hasattr(settings, 'EMAIL_TEMPLATES'):
        raise ImproperlyConfigured("Missing EMAIL_TEMPLATES in settings")

# Call this during app startup
validate_email_config()