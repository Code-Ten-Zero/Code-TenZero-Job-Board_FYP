from datetime import datetime
from App.models import CompanyAccount, JobListing, AlumnusAccount, AdminAccount, JobApplication, CompanySubscription, Notification
from App.database import db


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
    
    db.session.commit()
    return message