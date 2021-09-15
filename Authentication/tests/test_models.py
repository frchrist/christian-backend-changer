from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from Authentication.models import Client, ClientVerificationCode

class ClientAccountTest(APITestCase):

    def setUp(self):
        self.user1 = Client.objects.create(username="user1", email="user1@fmai.com", password="user1pass")
        self.user2 = Client.objects.create(username="user2", email="user2@fmai.com", password="user2pass")
    def test_create_client_account(self):
        """
        This test make that clients accounts are created
        """
        url = reverse("register")
        data = {"username":"christian", "password":"fakepassword", "email":"chr@gmail.com", "sponsor":""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), 3)
    def test_client_balance_is_null(self):
        self.assertEqual(Client.objects.first().balance, 0)

    def test_client_mail_is_verified_after_posted_right_code(self):
        url = reverse("verification_client_email")
        current_client = Client.objects.get(username="user1")
        code = ClientVerificationCode.objects.get(client=current_client)
        data = {"code":code.code}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertTrue(Client.objects.get(username="user1").email_is_valid)

    def test_client_is_not_admin(self):
        current_client = Client.objects.get(username="user2")
        self.assertEqual(current_client.is_staff, False)

    def test_username_is_not_posted(self):
        self.assertRaises(ValueError, Client.objects.create, username="",
                          email="mail@gmail.com", password="pass12345",
                          sponsor="")

    def test_email_is_not_posted(self):
        self.assertRaises(ValueError, Client.objects.create, username="mail",
                          email="", password="pass12345",
                          sponsor="")

    def test_register_core_expired_time(self):
        client = Client.objects.create(username="username", password="password", email="email@gmai.com" )
        code_instance = ClientVerificationCode.objects.get(client=client)
        code_instance.create_at = "2006-10-25 14:30:59"
        code_instance.save()
        response = self.client.post(reverse("verification_client_email"), {"code":code_instance.code}, format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

