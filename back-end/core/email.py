import os
from pathlib import Path
from fastapi import BackgroundTasks 
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType 

# settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", "7a99f3e51fbdb0"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", "e9e1f49b09fa93"),
    MAIL_PORT=os.environ.get("MAIL_PORT", 2525),
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "sandbox.smtp.mailtrap.io"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", True),
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", False),
    MAIL_DEBUG=True,
    MAIL_FROM=os.environ.get("MAIL_FROM", 'noreply@test.com'),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", "test"),
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", True)
)

fm = FastMail(conf)


async def send_email(recipients: list, subject: str, context: dict, template_name: str,
                     background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
