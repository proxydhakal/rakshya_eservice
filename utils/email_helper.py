# utils/email_helper.py
from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def send_email(
    api_key: str,
    to_email: str,
    to_name: str,
    sender_email: str,
    sender_name: str,
    subject: str,
    html_content: str
):
    """
    Helper function to send a single email via Brevo (Sendinblue) API.

    :param api_key: Your Brevo API key
    :param to_email: Recipient email
    :param to_name: Recipient name
    :param sender_email: Sender email
    :param sender_name: Sender name
    :param subject: Email subject
    :param html_content: HTML content of the email
    """
    # Configure API key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Create the email object
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        sender={"email": sender_email, "name": sender_name},
        subject=subject,
        html_content=html_content
    )

    try:
        response = api_instance.send_transac_email(email)
        return response
    except ApiException as e:
        print("Error sending email:", e)
        return None
