import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Reusable email notification service for all auth and order events."""

    @staticmethod
    def _send_html_email(subject, template_name, context, recipient_email):
        """Internal helper — sends HTML email with plain text fallback."""
        try:
            html_content = render_to_string(template_name, context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=f"{settings.EMAIL_SUBJECT_PREFIX}{subject}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"HTML Email sent to {recipient_email}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send HTML email to {recipient_email}: {e}")
            return False

    @classmethod
    def send_welcome_email(cls, user):
        """Sent after successful registration."""
        context = {
            'user': user,
            'site_url': settings.LOGIN_URL, # Adjust as needed
        }
        cls._send_html_email(
            subject="Welcome to Our Store!",
            template_name='emails/welcome_email.html',
            context=context,
            recipient_email=user.email,
        )

    @classmethod
    def send_order_confirmation(cls, user, order):
        """Sent when a user successfully places an order."""
        context = {
            'user': user,
            'order': order,
        }
        cls._send_html_email(
            subject=f"Order #{order.id} Confirmed",
            template_name='emails/order_confirmation.html',
            context=context,
            recipient_email=user.email,
        )

    @classmethod
    def send_login_notification(cls, user):
        """Sent when a user successfully logs in (Plain text for security alerts often preferred, but HTML for consistency)."""
        from datetime import datetime
        login_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        # For login notification, we can keep it simple or create another template
        # Let's just use the existing logic but wrapped in our new sender for consistency if needed
        # Or just keep it as is if text is fine. The user specifically asked for registration and order.
        pass

    @classmethod
    def send_logout_notification(cls, user):
        """Sent when a user logs out."""
        pass
