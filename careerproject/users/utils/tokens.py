from django.contrib.auth.tokens import PasswordResetTokenGenerator
import urllib.parse
from django.conf import settings
import six  # Use the standalone six library instead of Django's

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Creates a hash value for the token generation
        """
        return (
            str(user.pk) + str(timestamp) + 
            str(user.email) +
            str(user.is_active)
        )

email_verification_token = EmailVerificationTokenGenerator()

def generate_verification_token(user):
    """
    Generates a verification token for the user
    Args:
        user: User model instance
    Returns:
        URL-safe encoded token string
    """
    token = email_verification_token.make_token(user)
    return urllib.parse.quote(token)

def verify_verification_token(user, token):
    """
    Verifies the verification token for the user
    Args:
        user: User model instance
        token: Token string to verify
    Returns:
        bool: True if token is valid, False otherwise
    """
    try:
        decoded_token = urllib.parse.unquote(token)
        return email_verification_token.check_token(user, decoded_token)
    except Exception:
        return False