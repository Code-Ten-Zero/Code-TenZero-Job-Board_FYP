from App.models import AlumnusAccount, CompanyAccount, Notification
from App.database import db

from App.controllers.admin_account import get_all_admin_accounts

from App.models import CompanySubscription


def notify_subscribed_alumnus(message, company_id):
    company = CompanyAccount.query.get(company_id)

    if company:
        subscribed_alumni = CompanySubscription.query.filter_by(
            company_id=company.id).all()

        for subscription in subscribed_alumni:
            alumnus = AlumnusAccount.query.get(subscription.alumnus_id)

            if alumnus:
                new_notification = Notification(
                    alumnus_id=alumnus.id,
                    company_id=None,
                    admin_id=None,
                    message=message
                )
                db.session.add(new_notification)

    db.session.commit()
    return message


def notify_company_account(message, company_id):
    company = CompanyAccount.query.get(company_id)

    if company:
        new_notification = Notification(
            alumnus_id=None,
            company_id=company.id,
            admin_id=None,
            message=message
        )
        db.session.add(new_notification)
        db.session.commit()
    return message


def notify_admins(message):
    admins = get_all_admin_accounts()
    if admins:
        for admin in admins:
            new_notification = Notification(
                alumnus_id=None,
                company_id=None,
                admin_id=admin.id,
                message=message
            )
            db.session.add(new_notification)
        db.session.commit()
    return message
