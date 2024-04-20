from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword') # Log in the test user
        self.home_url = reverse('home')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.delete_user_url = reverse('delete_user')
        self.search_movies_url = reverse('search_movies')

    def test_home_page_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_delete_user_view(self):
        response = self.client.get(self.delete_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_user.html')

    def test_search_movies_view(self):
        response = self.client.get(self.search_movies_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_movies.html')

    def test_view_movie_details(self):
        movie_id = '123'
        url = reverse('view_movie_details', args=[movie_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_movie_details.html')