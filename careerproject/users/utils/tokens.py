import urllib.parse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  # Use the standalone six package

class PasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Create hash value for token generation
        Args:
            user: User instance
            timestamp: Current timestamp
        Returns:
            str: Hash value string
        """
        return (
            str(user.pk) + str(timestamp) + 
            str(user.password) +  # Invalidates when password changes
            str(user.is_active)
        )

# Create token generator instance
password_reset_token = PasswordResetTokenGenerator()

def generate_password_reset_token(user):
    """
    Generate URL-safe password reset token
    Args:
        user: User instance
    Returns:
        str: URL-encoded token
    """
    token = password_reset_token.make_token(user)
    return urllib.parse.quote(token)

def verify_password_reset_token(user, token):
    """
    Verify password reset token validity
    Args:
        user: User instance
        token: Token to verify
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        decoded_token = urllib.parse.unquote(token)
        return password_reset_token.check_token(user, decoded_token)
    except Exception:
        return False