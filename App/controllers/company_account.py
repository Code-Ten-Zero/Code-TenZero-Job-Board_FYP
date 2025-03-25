from App.models import CompanyAccount, JobListing, AlumnusAccount, AdminAccount, JobApplication
from App.database import db
from App.controllers import get_all_subscribed_alumni



def add_company(registered_name, password, login_email, mailing_address, phone_number, public_email, website_url):
    # Check if there are no other users with the same username or email values in any other subclass
        if (
            # Company.query.filter_by(email=email).first() is not None or
            AdminAccount.query.filter_by(login_email=login_email).first() is not None or
            AlumnusAccount.query.filter_by(login_email=login_email).first() is not None
            
        ):
            print("duplicate")
            return None  # Return None to indicate duplicates

        newCompany= CompanyAccount(login_email, password,registered_name, mailing_address, public_email, website_url, phone_number,profile_photo_file_path="N/A")
        try: # safetey measure for trying to add duplicate 
            db.session.add(newCompany)
            db.session.commit()  # Commit to save the new  to the database
            return newCompany
        except Exception as e:
            print(f"Rollback: {e}")
            db.session.rollback()
            return None

def add_listing(company_id, title, position_type, description,
                monthly_salary_ttd, is_remote, job_site_address, datetime_created, datetime_last_modified, admin_approval_status):

    # manually validate that the company actually exists
    company = get_company_by_id(company_id)
    if not company:
        return None

    newListing = JobListing(company_id, title, position_type, description, 
                monthly_salary_ttd, is_remote, job_site_address, datetime_created, datetime_last_modified, admin_approval_status)
    try:
        db.session.add(newListing)
        db.session.commit()

        # print('get_all_subscribed_alumn')
        # send_notification(job_categories)
        # send_notification(newListing.get_categories())

        # print('yah')
        return newListing
    except:
        # print('nah')
        db.session.rollback()
        return None
    
def get_company_by_id (id):
    return CompanyAccount.query.filter_by(id=id).first()

def get_company_by_email(login_email):
    return CompanyAccount.query.filter_by(login_email=login_email).first()

def get_company_listings(id):
    company = get_company_by_id(id)
    
    if company is None:
        raise ValueError(f"No company found")
    
    if not company.job_listings:
        return "No job listings found for this company."

    return company.job_listings

def get_all_companies():
    return CompanyAccount.query.all()

def get_all_companies_json():
    companies = get_all_companies()
    if not companies:
        return []
    companies = [company.get_json() for company in companies]
    return companies

def get_listing_job_applications(id):
    listing = JobListing.query.filter_by(id=id).first()
    
    if not listing:
        raise ValueError(f"Job listing with id {id} not found")
    
    listing_applications = JobApplication.query.filter_by(job_listing_id=listing.id).all()
    
    # Check if the list of applications is empty
    if not listing_applications:
        print("No applications found for this listing")
    
    return listing_applications

    