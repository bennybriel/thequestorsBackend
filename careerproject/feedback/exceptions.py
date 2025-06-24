class FeedbackServiceException(Exception):
    """Custom exception for feedback service errors"""
    pass

class FeedbackNotFoundException(Exception):
    """Raised when feedback is not found"""
    pass

class FeedbackValidationException(Exception):
    """Raised when feedback validation fails"""
    pass