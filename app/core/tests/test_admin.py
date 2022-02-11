from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='myemail@dev.com',
            password='unsecured'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="nosuper@lame.com",
            password="imsad",
            name='My test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # generates a url for the list user page
        # defined in the djgano admin documentation
        # "reverse" automatically updates the url for all tests
        # if it ever changes?
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)  # performs a http get on the url from above

        # implicitly checks that the status code is 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # generates a url like /admin/core/user/<id>
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
