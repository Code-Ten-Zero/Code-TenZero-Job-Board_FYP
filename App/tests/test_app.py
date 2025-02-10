import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Alumni, Company, Listing
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
    #add_categories,
    apply_listing,
    get_all_applicants,
    get_alumni,
    toggle_listing_approval,
    get_listing,
    get_approved_listings,
    get_company_by_name
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
        admin = Admin('bob', 'bobpass', 'bob@mail')
        assert admin.username == "bob"

    def test_new_alumni(self):
        alumni = Alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert alumni.username == 'rob'
    
    def test_new_company(self):
        company = Company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
        assert company.company_name == 'company1'

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = Admin("bob", password, 'bob@mail')
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = Admin("bob", password, 'bob@mail')
        assert user.check_password(password)

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
        assert login ("bobpass", 'bob@mail')!= None

    def test_create_admin(self):
        add_admin("bobpass", 'bob@mail')
        admin = add_admin("bobpass", 'rick@mail')
        assert admin.username == "rick"

    def test_create_alumni(self):
        alumni = add_alumni('robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert alumni.username == 'rob'

    def test_create_company(self):
        company = add_company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
        assert company.username == 'company1' and company.company_name == 'company1'

    # cz at the beginning so that it runs after create company
    def test_czadd_listing(self):
        listing = add_listing('listing1', 'listing1 description', 'company1', '8000', 'Full-time', True, True, 'desiredcandidate', 'curepe')
        assert listing.title == 'listing1' and listing.company_name == 'company1'

    def test_czsubscribe(self):

        alumni = subscribe('123456789', 'Database Manager')
        assert alumni.subscribed == True

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
            {"id":1,'email':'bob@mail'},
            {"id":2,'email':'rick@mail'},
            {"id":1,"email":"rob@mail", "alumni_id":123456789, "subscribed":True, "job_category":'Database Manager', 'contact':'1868-333-4444', 'firstname':'robfname', 'lastname':'roblname'},
            {"id":1, "company_name":"company1", "email":"company@mail", 'company_address':'company_address','contact':'contact',
            'company_website':'company_website.com'}
            ], users_json)

    def test_initial_has_seen_modal(self):
        alumni = add_alumni('alutest', 'alupass', 'alu@email.com', '911', '1800-273-8255', 'alufname', 'alulname')
        assert alumni.has_seen_modal == False

    def test_set_modal_seen(self):
        alumni = add_alumni('alutest2', 'alupass2', 'alu2@email.com', '912', '1868-273-8255', 'alu2fname', 'alu2lname')
        set_alumni_modal_seen(alumni.alumni_id)
        assert alumni.has_seen_modal == True


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

        company = get_company_by_name(job2.company_name)

        # Check if the notification was created
        notifications = company.notifications
        assert len(notifications) == 1
        assert notifications[0].message == f"Alumni {alumni.username} applied to your listing '{job2.title}'."