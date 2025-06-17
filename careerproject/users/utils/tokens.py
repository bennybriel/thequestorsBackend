from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import urllib.parse
from django.conf import settings

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + 
            six.text_type(user.email) +
            six.text_type(user.is_active)
        )

email_verification_token = EmailVerificationTokenGenerator()

def generate_verification_token(user):
    """
    Generates a verification token for the user
    """
    token = email_verification_token.make_token(user)
    # URL encode the token to make it safe for URLs
    return urllib.parse.quote(token)

def verify_verification_token(user, token):
    """
    Verifies the verification token for the user
    """
    # URL decode the token first
    decoded_token = urllib.parse.unquote(token)
    return email_verification_token.check_token(user, decoded_token)