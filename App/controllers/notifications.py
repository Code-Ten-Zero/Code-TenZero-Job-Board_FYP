
from datetime import datetime

from App.models import CompanyAccount, JobListing, AlumnusAccount, AdminAccount, JobApplication, CompanySubscription, Notification
from App.database import db

from App.controllers import (
    get_all_admins
)

from App.utils.email import send_email

def notify_subscribed_alumnus(message, company_id):
    company = CompanyAccount.query.get(company_id)
    
    if company:
        # Get all alumni subscribed to this specific company
        subscribed_alumni = CompanySubscription.query.filter_by(company_id=company.id).all()
        
        # Loop through all the subscribed alumni and send them a notification
        for subscription in subscribed_alumni:
            alumnus = AlumnusAccount.query.get(subscription.alumnus_id)
            
            if alumnus:
                # Create a notification for each subscribed alumnus
                new_notification = Notification(
                    alumnus_id=alumnus.id,
                    company_id=None,
                    admin_id=None, 
                    message=message
                )
                db.session.add(new_notification)
                send_email(alumnus.login_email, new_notification.message)
    
    db.session.commit()
    return message

#Used to send a specific company notifications
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
        send_email(company.login_email, new_notification.message)
    return message
                
#Used to send (all) admin notifications
def notify_admins(message):
    admins= get_all_admins()
    if admins:
        for admin in admins:
            new_notification = Notification(
            alumnus_id=None,
            company_id=None,
            admin_id=admin.id, 
            message=message
            )
            db.session.add(new_notification)
            send_email(admin.login_email, new_notification.message)
        db.session.commit()
    return message

