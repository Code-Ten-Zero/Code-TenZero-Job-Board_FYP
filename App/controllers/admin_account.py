from App.models import BaseUserAccount, AdminAccount, AlumnusAccount, CompanyAccount, JobListing
from App.database import db


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
    from .job_listing import get_listing

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
    from .job_listing import get_listing

    listing = get_listing(listing_id)

    if listing is not None:
        db.session.delete(listing)
        db.session.commit()
        return True

    return None

def toggle_listing_approval(listing_id, status):
    print("toggle listing approval function")
    from .job_listing import get_listing

    listing = get_listing(listing_id)
    if not listing:
        return None
    if status in ["APPROVED", "PENDING", "REJECTED"]:
        listing.admin_approval_status = status
    else:
        return None

    try:
        db.session.commit()
    except Exception as e:
        print(f'my error: {e}')
        db.session.rollback()
        return None


# def delete_exerciseSet(exerciseSet_id):

#     exerciseSets = ExerciseSet.query.filter_by(id=exerciseSet_id).all()

#     if exerciseSets is not None:
#         for exerciseSet in exerciseSets:
#             db.session.delete(exerciseSet)
        
#             db.session.commit()
#         return True
#     return None

# edit other listings