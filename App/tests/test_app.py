import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import BaseUserAccount, AdminAccount, AlumnusAccount, CompanyAccount, CompanySubscription, JobApplication, JobListing
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_email,
    update_user,
    add_admin,
    add_alumni,
    add_company,
    add_listing,
    subscribe,
    unsubscribe,
    add_categories,
    apply_listing,
    get_all_applicants,
    get_alumni,
    set_alumni_modal_seen,
    toggle_listing_approval,
    get_listing,
    get_approved_listings,
    get_company_by_email
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    # def test_new_user(self):
    #     user = User("bob", "bobpass")
    #     assert user.username == "bob"

    def test_new_admin(self):
        admin = AdminAccount('bob@mail','bobpass')
        assert admin.login_email == "bob@mail"

    def test_new_alumni(self):
        alumni = AlumnusAccount('rob@mail','robpass', 'robfname', 'roblname', '1868-333-4444')
        assert alumni.login_email == 'rob@mail'
    
    def test_new_company(self):
        company = CompanyAccount('company@mail', 'compass',  'company1', 'mailing_address', 'public@email','company_website.com','phone_number')
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
        self.assertDictEqual(user_json, {"id": None,"login_email": "bob@mail",
        "password_hash": "[HIDDEN]",
        "profile_photo_file_path": None })
    
    def test_generate_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = AdminAccount("bob@mail", password)
        assert user.password_hash != password

    def test_check_password(self):
        password = "mypass"
        user = AdminAccount('bob@mail',password)
        assert user.check_password(password)

    #test the retrieval of an admin account
    def test_get_admin_by_email(self):
        user = AdminAccount("bob@mail", "bobpass")
        print(get_user_by_email("bob@mail"))
        retreived_user = get_user_by_email("bob@mail")
        assert retreived_user.login_email == user.login_email

    #test the retrieval of an alumnus account
    def test_get_almunus_by_email(self):
        alumni = AlumnusAccount('rob@mail','robpass', 'robfname', 'roblname', '1868-333-4444')
        retreived_alumni = get_user_by_email("rob@mail")
        assert retreived_alumni.login_email == 'rob@mail'
    
    #test the retrieval of a company account
    def test_get_company_by_email(self):
        company = CompanyAccount('company@mail', 'compass',  'company1', 'mailing_address', 'public@email','company_website.com','phone_number')
        retreived_company = get_company_by_email("company@mail")
        assert retreived_company.login_email == company.login_email

    #test the behaviour of the retrieval fucntion of a user that does not exist 
    def test_get_user_by_email_not_found(self):
        retreived_user = get_user_by_email("unknown@mail")
        assert retreived_user is None
    

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


# def test_authenticate():
#     user = add_admin("bob", "bobpass", 'bob@mail')
#     assert login("bob", "bobpass") != None

class UserIntegrationTests(unittest.TestCase):

    def test_authenticate(self):
        user = add_admin("bobpass", 'bob@mail')
        assert login("bob@mail", "bobpass") != None

    def test_create_admin(self):
        add_admin("bobpass", 'bob@mail')
        admin = add_admin("bobpass", 'rick@mail')
        assert admin.login_email == "rick@mail"

    def test_create_alumni(self):
        my_alumni = add_alumni('robpass', 'robby2@mail', 'robfname', 'roblname', '1868-399-9944')
        assert my_alumni.login_email == "robby2@mail"

    def test_create_company(self):
        #add_company(registered_name, password, login_email, mailing_address, phone_number, public_email, website_url)
        company = add_company('company10', 'compass', 'company10@mail',  'mailing_address',
                'phone10_number', 'public10@email', 'company10_website.com')
        assert company.login_email == 'company10@mail' and company.public_email == 'public10@email'

    # cz at the beginning so that it runs after create company
    def test_czadd_listing(self):
        company1 = get_user_by_email('company@mail')
        listing =add_listing(company1.id, 'listing1','Part-time', 'job description1',
        8000, False, 'Curepe', '02-01-2025', '10-01-2025', 'PENDING')
        assert listing.description == 'job description1' and listing.monthly_salary_ttd == 8000

    #this was removed -CTZ
    # def test_czsubscribe(self):
    #     alumni = subscribe('123456789', 'Database Manager')
    #     assert alumni.subscribed == True

    # def test_czadd_categories(self):
    #     alumni = add_categories('123456789', ['Database'])
    #     assert alumni.get_categories() == ['Database']

    def test_czapply_listing(self):

        alumni = apply_listing('123456789', 1)

        assert get_all_applicants('1')  == [get_alumni('123456789')]


    # def get_all_applicants(self):
    #     applicants = get_all_applicants('1')

    

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([
            {"id":1, "username":"bob", 'email':'bob@mail'},
            {"id":2, "username":"rick", 'email':'rick@mail'},
            {"id":1, "username":"rob", "email":"rob@mail", "alumni_id":123456789, "subscribed":True, "job_category":'Database Manager', 'contact':'1868-333-4444', 'firstname':'robfname', 'lastname':'roblname'},
            {"id":1, "company_name":"company1", "email":"company@mail", 'company_address':'company_address','contact':'contact',
            'company_website':'company_website.com'}
            ], users_json)

    # def test_initial_has_seen_modal(self):
    #     alumni = add_alumni('alutest', 'alupass', 'alu@email.com', '911', '1800-273-8255', 'alufname', 'alulname')
    #     assert alumni.has_seen_modal == False

    # def test_set_modal_seen(self):
    #     alumni = add_alumni('alutest2', 'alupass2', 'alu2@email.com', '912', '1868-273-8255', 'alu2fname', 'alu2lname')
    #     set_alumni_modal_seen(alumni.alumni_id)
    #     assert alumni.has_seen_modal == True


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
        job = add_listing("Test Job", "Test Description", "company1", 8000, "Full-time", True, True, "bruzz", "Test Area")
        assert job.isApproved == False

    def test_toggle_listing_approval(self):
        job = add_listing("Test Job2", "Test Description", "company1", 8000, "Full-time", True, True, "huzz", "Test Area")

        result = toggle_listing_approval(job.id)

        listing = get_listing(job.id)
        assert result is True
        assert job.isApproved is True

    def test_get_approved_listings(self):
        job1 = add_listing("Approved Job", "Approved Job Description", "company1", 9000, "Full-time", True, True, "zach", "Approved Area")
        # job2 = add_listing("Unapproved Job", "Unapproved Job Description", "company1", 7000, "Part-time", False, True, "not zach", "Unapproved Area")

        job1.isApproved = True

        approved_listings = get_approved_listings()
        assert len(approved_listings) == 1
        assert approved_listings[0].id == job1.id

    def test_notify_observers(self):
        company = add_company('compaknee', 'compaknee', 'compassknee', 'compaknee@mail',  'compaknee_address', 'contactee', 'compaknee_website.com')
       
        alumni = add_alumni('alutest4', 'alupass4', 'alu4@email.com', '9114', '1800-274-8255', 'alufname4', 'alulname4')

        job2 = add_listing("Unapproved Job", "Unapproved Job Description", "compaknee", 7000, "Part-time", False, True, "not zach", "Unapproved Area")

        apply_listing(alumni.alumni_id, job2.id)

        company = get_company_by_email(job2.company.login_email)

        # Check if the notification was created
        notifications = company.notifications
        assert len(notifications) == 1
        assert notifications[0].message == f"Alumni {alumni.login_email} applied to your listing '{job2.title}'."