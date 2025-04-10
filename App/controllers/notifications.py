from App.models import AdminAccount, AlumnusAccount, CompanyAccount, Notification
from App.database import db
from App.utils.email import send_email
from sqlalchemy.exc import SQLAlchemyError


def notify_users(message: str, user_type: str, user_ids=None) -> str:
    """
    Sends notifications to users, both in-app and via email.

    Args:
        message (str): The message to be sent to users.
        user_type (str): The type of user to notify. Options: 'alumnus', 'company', 'admin'.
        user_ids (list): Optional list of user IDs. If None, all users of the specified type will be notified.

    Returns:
        str: The message that was sent.
    """
    user_models = {
        'alumnus': (AlumnusAccount, 'alumnus_id'),
        'company': (CompanyAccount, 'company_id'),
        'admin': (AdminAccount, 'admin_id')
    }

    if user_type:
        user_type = user_type.lower()
    if user_type not in user_models:
        raise ValueError(
            "Invalid user type. Must be 'alumnus', 'company', or 'admin'."
        )

    model, id_field = user_models[user_type]
    try:
        # Get users based on provided IDs or all users if user_ids is None
        users = model.query.filter(
            model.id.in_(user_ids) if user_ids else model.query
        ).all()

        for user in users:
            new_notification = Notification(
                alumnus_id=None, company_id=None, admin_id=None,
                message=message
            )
            setattr(new_notification, id_field, user.id)
            db.session.add(new_notification)
            send_email(user.login_email, "subject", message)

            db.session.commit()
            return message

    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Database error: {str(e)}"

    except Exception as e:
        return f"An error occurred: {str(e)}"
