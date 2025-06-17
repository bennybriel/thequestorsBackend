import requests
import json
from django.template.loader import render_to_string
from ..email.config import EMAIL_CONFIG
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(recipient, email_type, context=None):
        """
        General email sending method
        :param recipient: Email address of the recipient
        :param email_type: Key from EMAIL_CONFIG['TEMPLATES']
        :param context: Dictionary with template variables
        :return: Tuple (success: bool, response: dict)
        """
        if email_type not in EMAIL_CONFIG['TEMPLATES']:
            raise ValueError(f"Unknown email type: {email_type}")

        template_config = EMAIL_CONFIG['TEMPLATES'][email_type]
        
        # Render email content
        html_content = render_to_string(
            f"emails/{template_config['template_name']}",
            context or {}
        )

        headers = {
            "Authorization": EMAIL_CONFIG['API_TOKEN'],
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        payload = {
            "from": {
                "address": EMAIL_CONFIG['SENDER_EMAIL'],
                "name": "StalauTech"
            },
            "to": [{"email_address": {"address": recipient}}],
            "subject": template_config['subject'],
            "htmlbody": html_content
        }

        try:
            response = requests.post(
                EMAIL_CONFIG['API_URL'],
                headers=headers,
                data=json.dumps(payload))
            
            if response.status_code == 200:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {"error": str(e)}

    @staticmethod
    def send_signup_email(user, verification_url):
        """
        Specific method for sending signup emails
        :param user: User model instance
        :param verification_url: Email verification URL
        :return: Tuple (success: bool, response: dict)
        """
        context = {
            'user': user,
            'verification_url': verification_url,
            'support_email': 'support@stalautech.edu.ng'
        }
        return EmailService.send_email(
            recipient=user.email,
            email_type='SIGNUP',
            context=context
        )

    @staticmethod
    def send_password_reset_email(user, reset_url):
        """
        Specific method for sending password reset emails
        :param user: User model instance
        :param reset_url: Password reset URL
        :return: Tuple (success: bool, response: dict)
        """
        context = {
            'user': user,
            'reset_url': reset_url,
            'support_email': 'support@stalautech.edu.ng'
        }
        return EmailService.send_email(
            recipient=user.email,
            email_type='PASSWORD_RESET',
            context=context
        )