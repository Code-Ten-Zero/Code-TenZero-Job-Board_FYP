from App.models import JobListing, CompanyAccount, JobApplication
from App.database import db

# add in getters, maybe put setters in company controllers

def get_listing(id):
    return JobListing.query.filter_by(id=id).first()

def get_listing_title(listing_title):
    return JobListing.query.filter_by(title=listing_title).first()

def get_all_listings():
    return JobListing.query.all()

def get_all_applications(job_id):
    applications = JobApplication.query.filter_by(job_id=job_id).all()
    return applications

def get_all_listings_json():
    listings = get_all_listings()
    if not listings:
        return []
    listings = [listing.get_json() for listing in listings]
    return listings

# get all listings by company name