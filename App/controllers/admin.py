from App.models import User, Admin, Alumni, Company, Listing
from App.database import db


# create and add a new admin into the db
def add_admin(password, email):

    # Check if there are no other users with the same username or email values in any other subclass
        if (
            Company.query.filter_by(email=email).first() is not None or
            #Admin.query.filter_by(email=email).first() is not None
            Alumni.query.filter_by(email=email).first() is not None
        ):
            return None  # Return None to indicate duplicates

        newAdmin= Admin(password, email)
        try: # safety measure for trying to add duplicate 
            db.session.add(newAdmin)
            db.session.commit()  # Commit to save the new to the database
            return newAdmin
        except:
            db.session.rollback()
            return None

def delete_listing(listing_id):
    from .listing import get_listing

    listing = get_listing(listing_id)

    if listing is not None:
        db.session.delete(listing)
        db.session.commit()
        return True

    return None
    


def get_all_admins():
    return db.session.query(Admin).all()

def get_all_admins_json():
    admins = get_all_admins()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins

# delete other listings
def delete_listing(listing_id):
    from .listing import get_listing

    listing = get_listing(listing_id)

    if listing is not None:
        db.session.delete(listing)
        db.session.commit()
        return True

    return None

def toggle_listing_approval(listing_id):
    from .listing import get_listing

    listing = get_listing(listing_id)

    if listing is not None:
        current_state = listing.isApproved
        listing.isApproved = not current_state
        try:
            db.session.commit()
            if listing.isApproved:
                return True
            if not listing.isApproved: 
                return False
        except Exception as e:
            db.session.rollback()
            return None
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