import click
from flask.cli import AppGroup
from App.controllers.job_listing import (
    add_job_listing,
    get_all_job_listings,
    # delete_listing
)

job_listing_cli = AppGroup('listing', help='Listing object commands')


@job_listing_cli.command("list", help="Lists listings in the database")
@click.option("--jsonify-results", is_flag=True, help="Return results in JSON format")
def list_listing_command(jsonify_results):
    print(get_all_job_listings(jsonify_results))


# flask listing add
# Note: you have to manually enter in the job categories here eg: flask listing add listingtitle desc company1 Database


@job_listing_cli.command("add", help="Add listing object to the database")
@click.argument("company_id", default="company1.id")
@click.argument("title", default="Job offer 1")
@click.argument("postion-type", default="Full-time")
@click.argument("description", default="very good job :)")
@click.argument("monthly_salary_ttd", default="10000")
@click.argument("is_remote", default="True")
@click.argument("job_site_address", default="Curepe")
@click.argument("datetime_created", default="dd-mm-yy")
@click.argument("datetime_last_mmodified", default="dd-mm-yy")
@click.argument("admin_approval_status", default="PENDING")
def add_listing_command(company_id, title, position_type, description, monthly_salary_ttd, is_remote, job_site_address, datetime_created, datetime_last_modified, admin_approval_status):
    listing = add_job_listing(company_id, title, position_type, description, monthly_salary_ttd,
                          is_remote, job_site_address, datetime_created, datetime_last_modified, admin_approval_status)

    if listing is None:
        print(f'Error adding categories')
    else:
        print(f'{listing} added!')


# have to fix
# @job_listing_cli.command("delete", help="delete listing object from the database")
# @click.argument("id", default="1")
# def delete_listing_command(id):

#     # listing = get_listing(id)

#     deleted = delete_listing(id)

#     if deleted is not None:
#         print('Listing deleted')
#     else:
#         print('Listing not deleted')


@job_listing_cli.command("applicants", help="Get all applicants for the listing")
@click.argument("listing_id", default='1')
def get_listing_applicants_command(listing_id):
    applicants = get_all_applicants(listing_id)

    if applicants is None:
        print(f'Error getting applicants')
    else:
        print(applicants)
