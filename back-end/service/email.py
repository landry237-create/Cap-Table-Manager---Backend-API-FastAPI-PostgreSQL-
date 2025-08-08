from fastapi import BackgroundTasks
from Settings import get_settings
import models 
from core.email import send_email 
from utils.email_context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD

settings = get_settings()


async def send_account_verification_email(
    user: models.User,
    background_tasks: BackgroundTasks,
    person: models.Person
):
    """
    Sends an account verification email to a newly registered user.

    This function generates a verification token for the user, builds the
    account activation URL, prepares the email context, and schedules the
    sending of the verification email in the background.

    Parameters
    ----------
    user : models.User
        User object containing account details.
    background_tasks : BackgroundTasks
        Starlette/FastAPI background tasks instance for scheduling
        the email sending task.
    person : models.Person
        Person object containing personal details (e.g., first name, email).

    Returns
    -------
    None
    """

    from auth import hash_password
    string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = hash_password(string_context)
    activate_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={person.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": person.first_name,
        'activate_url': activate_url
    }
    subject = f"Account Verification - {settings.APP_NAME}"
    await send_email(
        recipients=[person.email],
        subject=subject,
        template_name="user/account-verification.html",
        context=data,
        background_tasks=background_tasks
    )
    
    
async def send_account_activation_confirmation_email(
    user: models.User,
    background_tasks: BackgroundTasks,
    person: models.Person
):
    """
    Sends an account activation confirmation email to the user.

    This function prepares the welcome email content and schedules the
    sending of the activation confirmation email in the background.

    Parameters
    ----------
    user : models.User
        User object containing account details.
    background_tasks : BackgroundTasks
        Starlette/FastAPI background tasks instance for scheduling
        the email sending task.
    person : models.Person
        Person object containing personal details (e.g., first name, email).

    Returns
    -------
    None
    """
    data = {
        'app_name': settings.APP_NAME,
        "name": person.first_name,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[person.email],
        subject=subject,
        template_name="user/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks
    )
    
async def send_password_reset_email(
    user: models.User,
    background_tasks: BackgroundTasks,
    person: models.Person
):
    """
    Sends a password reset email to the user.

    This function generates a password reset token for the user, builds the
    reset URL, prepares the email context, and schedules the sending of the
    reset email in the background.

    Parameters
    ----------
    user : models.User
        User object containing account details.
    background_tasks : BackgroundTasks
        Starlette/FastAPI background tasks instance for scheduling
        the email sending task.
    person : models.Person
        Person object containing personal details (e.g., first name, email).

    Returns
    -------
    None
    """
    from auth import hash_password
    string_context = user.get_context_string(context=FORGOT_PASSWORD)
    token = hash_password(string_context)
    reset_url = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={person.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": person.first_name,
        'activate_url': reset_url,
    }
    subject = f"Reset Password - {settings.APP_NAME}"
    await send_email(
        recipients=[person.email],
        subject=subject,
        template_name="user/password-reset.html",
        context=data,
        background_tasks=background_tasks
    )