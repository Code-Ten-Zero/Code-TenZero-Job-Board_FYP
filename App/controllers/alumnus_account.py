from App.models import BaseUserAccount, AlumnusAccount, AdminAccount, CompanyAccount, JobListing
from App.database import db


def add_alumni(password, login_email, first_name, last_name, phone_number):


        # Check if there are no other users with the same email values in any other subclass
        if (
            # Alumni.query.filter_by(username=username).first() is not None or
            AdminAccount.query.filter_by(login_email=login_email).first() is not None or
            CompanyAccount.query.filter_by(login_email=login_email).first() is not None 
        ):
            return None  # Return None to indicate duplicates

        newAlumni= AlumnusAccount(login_email, password, first_name, last_name, phone_number)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newAlumni)
            print("alumni added successfully")
            db.session.commit()  # Commit to save the new  to the database
            return newAlumni
        except:
            db.session.rollback()
            return None

def get_all_alumni():
    return db.session.query(AlumnusAccount).all()

def get_all_alumni_json():
    alumnis = get_all_alumni()
    if not alumnis:
        return []
    alumnis = [alumni.get_json() for alumni in alumnis]
    return alumnis

def get_alumni(id):
    return AlumnusAccount.query.filter_by(id=id).first()

## to be re written entirely later -CTZ
def is_alumni_subscribed(id):
    # alumni = get_alumni(id)
    # if(alumni.subscribed == True):
    #     return True
    # else:
    return False


# also needs to be rewritten entirely -CTZ
def get_all_subscribed_alumni():
    return get_all_alumni()
    # all_alumni = AlumnusAccount.query.filter_by(subscribed=True).all()
    # return all_alumni


# Also needs to be re written -CTZ
# handle subscribing and unsubscribing, this needs to be changed to handle subscribing to companies
def subscribe(id, job_category=None):
    alumni = get_alumni(id)

    # if alumni is None:
    #     print('nah')
    #     return None
    
    # alumni.subscribed = True

    # if job_category is not None:
    #     # add_categories(alumni_id, job_category)
    #     alumni.add_category(job_category)

    # db.session.add(alumni)
    # db.session.commit()
    return alumni

## rewrite me -CTZ
def unsubscribe(id):
    alumni = get_alumni(id)

    # if not alumni:
    #     # print('nah')
    #     return None

    # alumni.subscribed = False
    # remove_categories(id, alumni.get_categories())

    # db.session.add(alumni)
    # db.session.commit()
    return alumni

# def subscribe_action(alumni_id, job_category=None):
#     alumni = get_alumni(alumni_id)

#     if not alumni:
#         # print('nah')
#         return None
    
#     # if they are already susbcribed then unsubscribe them
#     if is_alumni_subscribed(alumni_id):
#         alumni.subscribed = False
#         remove_categories(alumni_id, alumni.get_categories())
    
#     else:
#         alumni.subscribed = True

#         if job_category is not None:
#             add_categories(alumni_id, job_category)
#         # set their jobs list to job_category ?

#     db.session.add(alumni)
#     db.session.commit()
#     return alumni
        
# adding and removing job categories 
def add_categories(id, job_categories):
    alumni = get_alumni(id)
    try:
        for category in job_categories:
            # print(category)
            alumni.add_category(category)
            # print(alumni.get_categories())
            db.session.commit()
        return alumni
    except:
        db.session.rollback()
        return None   

def remove_categories(id, job_categories):
    alumni = get_alumni(id)
    try:
        for category in job_categories:
            alumni.remove_category(category)
            db.session.commit()
        return alumni
    except:
        db.session.rollback()
        return None

# apply to an application
# def apply_listing(alumni_id, listing_title):
def apply_listing(id, joblisting_id):
    from App.controllers import get_listing, get_company_by_name

    alumni = get_alumni(id)

    # error check to see if alumni exists
    if alumni is None:
        # print('is none')
        return None

    # get the listing and then company that made the listing
    listing = get_listing(joblisting_id)

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


def set_alumni_modal_seen(id):
    alumni = get_alumni(id)
    alumni.has_seen_modal = True
    db.session.commit()
    
# To be re written - CTZ
def get_approved_listings():
    return JobListing.query.all()


def update_alumni_info(id, first_name, last_name, phone_number, login_email, current_password, new_password):
    alumni = get_alumni(id)
    update_made = False

    if alumni.check_password(current_password):
        if alumni.first_name != first_name:
            alumni.first_name = first_name
            update_made = True

        if alumni.last_name != last_name:
            alumni.last_name = last_name
            update_made = True

        if alumni.phone_number != phone_number:
            alumni.phone_number = phone_number
            update_made = True

        if alumni.login_email != login_email:
            alumni.login_email = login_email
            update_made = True

        if new_password != None: 
            alumni.set_password(new_password)
            update_made = True

    if update_made:
        db.session.commit()

    return update_made

