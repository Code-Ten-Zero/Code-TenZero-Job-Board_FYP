from App.models import User, Alumni, Admin, Company, Listing
from App.database import db


def add_alumni(password, email, phone_number, firstname, lastname):

        # Check if there are no other users with the same username or email values in any other subclass
        if (

            Company.query.filter_by(email=email).first() is not None or
            Admin.query.filter_by(email=email).first() is not None
            # Alumni.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newAlumni= Alumni(password, email, phone_number, firstname, lastname)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAlumni)
            db.session.commit()  # Commit to save the new  to the database
            return newAlumni
        except:
            db.session.rollback()
            return None

def get_all_alumni():
    return db.session.query(Alumni).all()

def get_all_alumni_json():
    alumnis = get_all_alumni()
    if not alumnis:
        return []
    alumnis = [alumni.get_json() for alumni in alumnis]
    return alumnis

def get_alumni(alumni_id):
    return Alumni.query.filter_by(alumni_id=alumni_id).first()

def is_alumni_subscribed(alumni_id):
    alumni = get_alumni(alumni_id)

    if(alumni.subscribed == True):
        return True
    else:
        return False

def get_all_subscribed_alumni():
    all_alumni = Alumni.query.filter_by(subscribed=True).all()
    return all_alumni

# handle subscribing and unsubscribing
def subscribe(alumni_id, job_category=None):
    alumni = get_alumni(alumni_id)

    if alumni is None:
        print('nah')
        return None
    
    alumni.subscribed = True

    if job_category is not None:
        # add_categories(alumni_id, job_category)
        alumni.add_category(job_category)

    db.session.add(alumni)
    db.session.commit()
    return alumni

def unsubscribe(alumni_id):
    alumni = get_alumni(alumni_id)

    if not alumni:
        # print('nah')
        return None

    alumni.subscribed = False
    remove_categories(alumni_id, alumni.get_categories())

    db.session.add(alumni)
    db.session.commit()
    return alumni

# apply to an application
# def apply_listing(alumni_id, listing_title):
def apply_listing(alumni_id, listing_id):
    from App.controllers import get_listing_title, get_listing, get_company_by_name

    alumni = get_alumni(alumni_id)

    # error check to see if alumni exists
    if alumni is None:
        # print('is none')
        return None

    # get the listing and then company that made the listing
    # listing = get_listing_title(listing_title)
    listing = get_listing(listing_id)

    if listing is None:
        return None

    # add the alumni to the listing applicant
    listing.applicant.append(alumni)
    alumni.listing.append(listing)

    company = get_company_by_name(listing.company_name)

    #commit changes to the database
    db.session.commit()

    listing.notify_observers(alumni, company)

    # add the alumni as an applicant to the company model object?

    return alumni

    
# only view approved listings
def get_approved_listings():
    return Listing.query.filter_by(isApproved=True).all()
