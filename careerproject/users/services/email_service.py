# email/service.py
from django.conf import settings
from django.template.loader import render_to_string
from ..email.configs import get_email_config
import requests
import json
from rest_framework import status
from rest_framework.response import Response

class EmailService:
    @staticmethod
    def send_email(recipient,name,email_type, url, context=None):
        """
        General email sending method using settings configuration
        """
        config = get_email_config()
       
       
        if not config:
            raise ValueError("Email configuration not found in settings")
        
        if email_type not in config.get('TEMPLATES', {}):
            raise ValueError(f"Unknown email type: {email_type}")

        template_config = config['TEMPLATES'][email_type]
        
        # Render email content
        # html_content = render_to_string(
        #     f"emails/{template_config['template_name']}",
        #     context or {}
        # )
        
        headers = {
            "Authorization": config['API_TOKEN'],
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        email_templates = {
            "SIGNUP": {
                "subject": "Account Signup",
                "htmlbody": f"""
                    <html>
                        <body>
                            <h3>Dear {name},</h3>
                            <p>Thank you for joining The Questors! We’re thrilled to have you on board.</p>
                            <p>Your account has been successfully created</p>
                            
                            <a href="{url}" 
                               style="background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">
                                Signin to your account
                            </a>
                            <p>If you didn't sign up, you can ignore this email.</p>
                        </body>
                    </html>
                """,
            },
            "PASSWORD_RESET": {
                "subject": "Password Reset Request",
                "htmlbody": f"""
                    <html>
                        <body>
                            <h3>Dear {name},</h3>
                            <p>Click the button below to reset your password:</p>
                            <a href="{url}" 
                               style="background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">
                                Reset Password
                            </a>
                            <p>If you didn’t request this, you can ignore this email.</p>
                        </body>
                    </html>
                """,
            },
            "application_completed": {
                "subject": "Application Completion Notification",
                "htmlbody": f"""
                    <html>
                        <body>
                            <h3>Dear {name},</h3>
                            <p>This is to notify you that your application has been successfully completed and received. 
                            Please log in to start tracking your application progress.</p>
                        </body>
                    </html>
                """,
            },
             "general_notification": {
                "subject": "Important Notification",
                "htmlbody": f"""
                    <html>
                        <body>
                            <h3>Hi {name},</h3>
                            <p>We have an important update for you. Please log in to your account to check the details.</p>
                        </body>
                    </html>
                """,
            },
            
        }

        if email_type not in email_templates:
            return Response({"error": "Invalid email type"}, status=status.HTTP_400_BAD_REQUEST)

        email_data = email_templates[email_type]
        #print(email_data)
        

        payload = {
            #"template_key": "2d6f.7712171af2cd96e.k1.daa0eb10-526c-11f0-8c4e-86f7e6aa0425.197ab7d1c41",
            "from": {
                "address": config['SENDER_EMAIL'],
                "name": "The Questors"
            },
            "to": [{"email_address": {"address": recipient}}],
            "subject": template_config['subject'],
            "htmlbody":  email_data["htmlbody"],
        }
      
        try:
           
            response = requests.post(config['API_URL'], json=payload, headers=headers)
            print(response.json())
            if response.status_code == 201:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {"error": str(e)}

    @staticmethod
    def send_signup_email(user, verification_url):
        """
        Specific method for sending signup emails
        """
        context = {
            'user': user,
            'verification_url': verification_url,
            'support_email': 'support@thequestors.com'
        }
        return EmailService.send_email(
            recipient=user.email,
            name=user.first_name,
            email_type='SIGNUP', 
            url=verification_url,
            context=context,
           
        )

    @staticmethod
    def send_password_reset_email(user, reset_url):
        """
        Specific method for sending password reset emails
        """
        context = {
            'user': user,
            'reset_url': reset_url,
            'support_email': 'support@questors.com'
        }
        return EmailService.send_email(
            recipient=user.email,
            name=user.first_name,
            email_type='PASSWORD_RESET',
            url=reset_url,
            context=context
        )