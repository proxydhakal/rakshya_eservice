# utils/email_helper.py
from django.core.mail import EmailMultiAlternatives

def send_email(
    subject: str,
    to_email: str,
    to_name: str,
    sender_email: str,
    sender_name: str,
    html_content: str,
    text_content: str = None,
):
    """
    Helper function to send an email using Django's EmailMultiAlternatives.
    """
    # If no plain text is provided, strip tags as fallback
    if not text_content:
        import re
        text_content = re.sub(r"<[^>]*>", "", html_content)

    from_email = f"{sender_name} <{sender_email}>"
    recipient = [f"{to_name} <{to_email}>"]

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
