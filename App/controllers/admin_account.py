from App.models import AdminAccount, AlumnusAccount, CompanyAccount, JobListing, CompanySubscription
from App.database import db
from .job_listing import get_listing

# create and add a new admin into the db
def add_admin(password, login_email):

    # Check if there are no other users with the same email values in any other subclass
        if (
            AlumnusAccount.query.filter_by(login_email=login_email).first() is not None or
            # Admin.query.filter_by(email=email).first() is not None or
            CompanyAccount.query.filter_by(login_email=login_email).first() is not None 
        ):
            return None  # Return None to indicate duplicates

        newAdmin= AdminAccount(login_email,password,profile_photo_file_path="N/A")
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAdmin)
            db.session.commit()  # Commit to save the new to the database
            return newAdmin
        except:
            db.session.rollback()
            return None

def delete_listing(jobListing_id):

    joblisting = get_listing(jobListing_id)

    if joblisting is not None:
        db.session.delete(joblisting)
        db.session.commit()
        return True

    return None

def get_admin(id):
    return AdminAccount.query.filter_by(id=id).first()

def get_all_admins():
    return db.session.query(AdminAccount).all()

def get_all_admins_json():
    admins = get_all_admins()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins

# delete other listings
def delete_listing(listing_id):

    listing = get_listing(listing_id)

    if listing is not None:
        db.session.delete(listing)
        db.session.commit()
        return True

    return None

def toggle_listing_approval(listing_id, status):
    print("toggle listing approval function")

    listing = get_listing(listing_id)
    if not listing:
        return None
    if status in ["APPROVED", "PENDING", "REJECTED", "DELETION REQUESTED", "UPDATE REQUESTED"]:
        listing.admin_approval_status = status
    else:
        return None

    try:
        db.session.commit()
        return True
    except Exception as e:
        print(f'my error: {e}')
        db.session.rollback()
        return None

