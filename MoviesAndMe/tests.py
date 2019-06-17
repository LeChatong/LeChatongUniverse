from django.urls import reverse
from django.test import TestCase

# Create your tests here.
class HomePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)