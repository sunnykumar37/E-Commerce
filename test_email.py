import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_app.settings')
django.setup()

def test_email():
    print(f"DEBUG: EMAIL_HOST={settings.EMAIL_HOST}")
    print(f"DEBUG: EMAIL_PORT={settings.EMAIL_PORT}")
    print(f"DEBUG: EMAIL_HOST_USER={settings.EMAIL_HOST_USER}")
    # Don't print the whole password, but print its length and first/last char
    pwd = settings.EMAIL_HOST_PASSWORD
    print(f"DEBUG: EMAIL_HOST_PASSWORD length={len(pwd)}")
    if len(pwd) > 2:
        print(f"DEBUG: EMAIL_HOST_PASSWORD starts with '{pwd[0]}' and ends with '{pwd[-1]}'")
    
    print(f"Attempting to send test email to {settings.EMAIL_HOST_USER}...")
    try:
        send_mail(
            'Test Email',
            'This is a test email from the Django project.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("Success! Test email sent.")
    except Exception as e:
        print(f"Error sending test email: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_email()
