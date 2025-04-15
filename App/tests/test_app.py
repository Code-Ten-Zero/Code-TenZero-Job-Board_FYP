import pytest
import logging
import unittest
from werkzeug.security import generate_password_hash, check_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import AdminAccount, AlumnusAccount, CompanyAccount

from App.controllers.auth import login
from App.controllers.base_user_account import get_user_by_email
from App.controllers import (
    add_admin_account,
    add_alumnus_account,
    add_company_account,
    add_job_listing,
    get_all_users_json,
    get_approved_listings,
    get_company_account_by_login_email,
    get_job_listing,
    get_user_by_email,
    toggle_listing_approval,
    company_subscription,
    add_company_subscription,
    get_company_subscriptions_by_alumnus_id,
    delete_company_subscription,
    update_alumnus_account
)


LOGGER = logging.getLogger(__name__)

'''
Unit Tests
'''


class UserUnitTests(unittest.TestCase):
    def test_new_admin(self):
        admin = AdminAccount('bob@mail', 'bobpass')
        assert admin.login_email == "bob@mail"

    def test_new_alumnus(self):
        alumnus = AlumnusAccount(
            'rob@mail',
            'robpass',
            'robfname',
            'roblname',
            '1868-333-4444'
        )
        assert alumnus.login_email == 'rob@mail'

    def test_new_company(self):
        company = CompanyAccount(
            'company@mail',
            'compass',
            'company1',
            'mailing_address',
            'public@email',
            'company_website.com',
            'phone_number'
        )
        assert company.login_email == 'company@mail'

    # # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = AdminAccount("bob@mail", "bobpass")
    #     user_json = user.__json__()
    #     self.assertDictEqual(user_json, {"id":None, "login_email":"bob@mail", 'password':'bobpass'})

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = AdminAccount("bob@mail", "bobpass")
        user_json = user.__json__()
        self.assertDictEqual(
            user_json,
            {
                "id": None,
                "login_email": "bob@mail",
                "password_hash": "[HIDDEN]",
                "profile_photo_file_path": "profile-images/anonymous-profile.png"
            }
        )


def test_generate_hashed_password():
    password = "bobpass"
    user = AdminAccount("bob@mail.com", password)
    assert check_password_hash(user.password_hash, password)

    def test_check_password(self):
        password = "mypass"
        user = AdminAccount('bob@mail.com', password)
        assert user.check_password(password)

    # test the retrieval of an admin account
    def test_get_admin_by_email(self):
        user = AdminAccount("bob@mail.com", "bobpass")
        print(get_user_by_email("bob@mail.com"))
        retreived_user = get_user_by_email("bob@mail.com")
        assert retreived_user.login_email == user.login_email

    # test the retrieval of an alumnus account
    def test_get_almunus_by_email(self):
        alumnus = AlumnusAccount(
            'rob@mail.com',
            'robpass',
            'robfname',
            'roblname',
            '1868-333-4444'
        )
        retreived_alumnus = get_user_by_email("rob@mail.com")
        assert retreived_alumnus.login_email == 'rob@mail.com'

    # test the retrieval of a company account
    def test_get_company_by_email(self):
        company = CompanyAccount(
            'company@mail.com',
            'compass',
            'company1',
            'mailing_address',
            'public@email.com',
            'company_website.com',
            'phone_number'
        )
        retreived_company = get_company_account_by_login_email("company@mail.com")
        assert retreived_company.login_email == company.login_email

    # test the behaviour of the retrieval fucntion of a user that does not exist
    def test_get_user_by_email_not_found(self):
        retreived_user = get_user_by_email("unknown@mail.com")
        assert retreived_user is None


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app(
        {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'}
    )
    create_db()
    yield app.test_client()
    db.drop_all()


# def test_authenticate():
#     user = add_admin("bob", "bobpass", 'bob@mail')
#     assert login("bob", "bobpass") != None

class UserIntegrationTests(unittest.TestCase):

    def test_authenticate(self):
        add_admin_account('bob2@mail.com', "bobpass")
        assert login("bob2@mail.com", "bobpass") != None

    def test_create_admin(self):
        add_admin_account('bob3@mail.com', "bobpass")
        admin = add_admin_account('rick2@mail.com', "bobpass")
        assert admin.login_email == "rick2@mail.com"

    def test_create_alumnus(self):
        my_alumnus = add_alumnus_account(
            'robby2@mail.com',
            'robpass',
            'robfname',
            'roblname',
            '1868-399-9944'
        )
        assert my_alumnus.login_email == "robby2@mail.com"

    def test_create_company(self):
        company = add_company_account(
            'company10@mail.com',
            'compass',
            'company10',
            'mailing_address',
            'public10@email.com',
            'company10_website.com',
            'phone10_number'
        )
        assert company.login_email == 'company10@mail.com' and company.public_email == 'public10@email.com'

    # cz at the beginning so that it runs after create company
    def test_czadd_listing(self):
        company1 = get_user_by_email('company10@mail.com')
        listing = add_job_listing(
            company1.id,
            'listing1',
            'Part-time',
            'job description1',
            8000,
            False,
            'Curepe'
        )
        assert listing.description == 'job description1' and listing.monthly_salary_ttd == 8000

    # this was removed -CTZ
    # def test_czsubscribe(self):
    #     alumnus = subscribe('123456789', 'Database Manager')
    #     assert alumnus.subscribed == True

    # def test_czadd_categories(self):
    #     alumnus = add_categories('123456789', ['Database'])
    #     assert alumnus.get_categories() == ['Database']

    # apply method to be updated
    # def test_czapply_listing(self):
    #     alumnus = apply_listing('123456789', 1)
    #     assert get_all_applicants('1')  == [get_alumnus('123456789')]

    # def get_all_applicants(self):
    #     applicants = get_all_applicants('1')

    def test_get_all_users_json(self):
        print(get_all_users_json())
        users_json = get_all_users_json()
        self.assertListEqual([
            {'id': 1, 
            'login_email': 'bob2@mail.com', 
            'password_hash': '[HIDDEN]', 
            'profile_photo_file_path': 'profile-images/anonymous-profile.png'},

            {'id': 2, 
            'login_email': 'bob3@mail.com', 
            'password_hash': '[HIDDEN]', 
            'profile_photo_file_path': 'profile-images/anonymous-profile.png'}, 

            {'id': 3, 
            'login_email': 'rick2@mail.com', 
            'password_hash': '[HIDDEN]', 
            'profile_photo_file_path': 'profile-images/anonymous-profile.png'}, 

            {'id': 1, 
            'login_email': 'robby2@mail.com', 
            'password_hash': '[HIDDEN]', 
            'first_name': 'robfname', 
            'last_name': 'roblname', 
            'phone_number': '1868-399-9944', 
            'profile_photo_file_path': 'profile-images/anonymous-profile.png'}, 

            {'id': 1, 
            'Login Email': 'company10@mail.com', 
            'password_hash': '[HIDDEN]', 
            'registered_name': 'company10', 
            'mailing_address': 'mailing_address', 
            'public_email': 'public10@email.com', 
            'website_url': 'company10_website.com', 
            'phone_number': 'phone10_number', 
            'profile_photo_file_path': 'profile-images/anonymous-profile.png'}
        ],
            users_json
        )

    # def test_initial_has_seen_modal(self):
    #     alumnus = add_alumnus('alutest', 'alupass', 'alu@email.com', '911', '1800-273-8255', 'alufname', 'alulname')
    #     assert alumnus.has_seen_modal == False

    # def test_set_modal_seen(self):
    #     alumnus = add_alumnus('alutest2', 'alupass2', 'alu2@email.com', '912', '1868-273-8255', 'alu2fname', 'alu2lname')
    #     set_alumnus_modal_seen(alumnus.alumnus_id)
    #     assert alumnus.has_seen_modal == True

    # def test_create_user(self):
    #     user = create_user("rick", "bobpass")
    #     assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"

    def test_initial_isapproved(self):
        company2 = get_user_by_email('company10@mail.com')
        job = add_job_listing(
            company2.id,
            'listing2',
            'Full-time',
            'job description2',
            4000,
            False,
            'Port-Of-Spain'
        )
        assert job.admin_approval_status == "PENDING"

    def test_toggle_listing_approval(self):
        company2 = get_user_by_email('company10@mail.com')
        job = add_job_listing(
            company2.id,
            'listing4',
            'Full-time',
            'job description3',
            4000,
            False,
            'San-Fernando'
        )
        toggle_listing_approval(job.id, "APPROVED")
        toggled_job = get_job_listing(job.id)
        assert toggled_job.admin_approval_status == "APPROVED"

    def test_get_approved_listings(self):
        company2 = get_user_by_email('company10@mail.com')
        job = add_job_listing(
            company2.id,
            'listing5',
            'Full-time',
            'job description3',
            4000,
            False,
            'San-Fernando'
        )

        job.admin_approval_status = "APPROVED"

        approved_listings = get_approved_listings()
        assert len(approved_listings) == 1
        assert approved_listings[0].id == job.id

    def test_subscribe(self):
        #print (add_company_subscription(1,1))
        #print (get_company_subscriptions_by_alumnus_id (1,True))
        company2 = get_user_by_email('company10@mail.com')
        user = get_user_by_email('robby2@mail.com')
        add_company_subscription(user.id,company2.id)
        assert get_company_subscriptions_by_alumnus_id (1,True) == [{'alumnus_id': {1}, 'company_id': {1}}]

    def test_sva_delete_subscription_invalid(self):
        company2 = get_user_by_email('company10@mail.com')
        user = get_user_by_email('robby2@mail.com')
        adminID = 9
        delete_company_subscription( 9, 9, 9)
        print (get_company_subscriptions_by_alumnus_id (1,True))
        assert get_company_subscriptions_by_alumnus_id(1,True) == [{'alumnus_id': {1}, 'company_id': {1}}]

    def test_svb_delete_subscription(self):
        company2 = get_user_by_email('company10@mail.com')
        user = get_user_by_email('robby2@mail.com')
        adminID = 1
        delete_company_subscription( 1, 1, 1)
        print (get_company_subscriptions_by_alumnus_id (1,True))
        assert get_company_subscriptions_by_alumnus_id(1,True) == []

    def test_update_alumni(self):
        user = get_user_by_email('robby2@mail.com')
        update_alumnus_account (user.id,"robnewfname","","","","robpass","","")
        updated_user = get_user_by_email('robby2@mail.com')
        assert updated_user.first_name == "robnewfname"

#    def test_delete_job_listing(self):





    






# ctz removed till subscriptions and notifications fixed
    # def test_notify_observers(self):
    #     company = add_company_account('compaknee', 'compaknee', 'compassknee', 'compaknee@mail',  'compaknee_address', 'contactee', 'compaknee_website.com')
    #     alumnus = add_alumnus('alutest4', 'alupass4', 'alu4@email.com', '9114', '1800-274-8255', 'alufname4', 'alulname4')
    #     job2 = add_listing("Unapproved Job", "Unapproved Job Description", "compaknee", 7000, "Part-time", False, True, "not zach", "Unapproved Area")
    #     apply_listing(alumnus.alumnus_id, job2.id)
    #     company = get_company_by_email(job2.company.login_email)
    #     # Check if the notification was created
    #     notifications = company.notifications
    #     assert len(notifications) == 1
    #     assert notifications[0].message == f"Alumnus {alumnus.login_email} applied to your listing '{job2.title}'."
