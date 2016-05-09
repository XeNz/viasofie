from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver

class AdminTestCase(LiveServerTestCase):
    def setUp(self):
        #Instanciate the selenium webdriver and load the webbrowser.
        User.objects.create_superuser(
                                      username='admin',
                                      password='admin',
                                      email='admin@example.com'
                                      )

        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(AdminTestCase, self).setUp()


    def teardown(self):
        #Call teardown to close the webbrowser.
        self.selenium.quit()
        super(AdminTestCase, self).teardown()



    def test_create_user(self):
        """
        Django admin create user test.
        This test will create a user in django admin and assert that the
        page is redirected to the new user change form.
        """
        #open the django admin page.
        self.selenium.get(
                          '%s%s' % (self.live_server_url, "/admin")
                          )

        #fill in login information of admin
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys("admin")
        password = self.selenium.find_element_by_id("id_password")
        password.send_keys("admin")

        #locate login button and click it.
        self.selenium.find_element_by_xpath('//input[@value="Inloggen"]').click()
        self.selenium.get(
                          '%s%s' % (self.live_server_url, "/admin/auth/user/add/")
                          )

        # Fill the create user form with username and password
        self.selenium.find_element_by_id("id_username").send_keys("test")
        self.selenium.find_element_by_id("id_password1").send_keys("test")
        self.selenium.find_element_by_id("id_password2").send_keys("test")

        # Forms can be submitted directly by calling its method submit
        self.selenium.find_element_by_id("user_form").submit()
        self.assertIn("Change user", self.selenium.title)
