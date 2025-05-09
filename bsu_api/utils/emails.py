import aiosmtplib
import logging
import functools
from email.message import EmailMessage

log = logging.getLogger(__name__)


async def send_notification(to_: str, content: str) -> None:
    """
    Send a notification email to the specified recipient.

    Args:
        to_ (str): The recipient's email address.
        content (str): The message content to be sent.

    Returns:
        None
    """

    email_content = (
        "Dear User,\n\n"
        "You have received a new notification:\n\n"
        f"{content}\n\n"
        "Best regards,\n"
        "BSU Warehouse (AI Team)"
    )

    message = EmailMessage()
    message["From"] = ""
    message["To"] = to_
    message["Subject"] = "New Notification from BSU Warehouse"
    message.set_content(email_content)

    try:
        await aiosmtplib.send(
            message,
            hostname="",
            port=587,
            username="",
            password="",
            use_tls=True,
        )
    except Exception as e:
        log.error(f"Failed to send customer email: {e}")
