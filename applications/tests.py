from django.test import TestCase
from .models import Application
from django.contrib.auth.models import User


# Create your tests here.

class UserTestCase(TestCase):
    def test_signup(self):
        response = self.client.post('/signup/', {
            'username' : 'testuser',
            'password1' : 'someStrongPassword123',
            'password2' : 'someStrongPassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_see_user_application(self):
        userA = User.objects.create_user(username='usera', password='passwordA123')
        userB = User.objects.create_user(username='userb', password='passwordB123')

        applicationA = Application.objects.create(
            user=userA,
            company='companyA',
            role='Software',
            status='applied',
            applied_date='2026-02-01'
        )
        applicationB = Application.objects.create(
            user=userB,
            company='companyB',
            role='Consulting',
            status='ghosted',
            applied_date='2026-02-01'
        )

        self.client.login(username='usera', password='passwordA123')
        response = self.client.get('/applications/')

        self.assertContains(response, 'companyA')
        self.assertNotContains(response, 'companyB')


