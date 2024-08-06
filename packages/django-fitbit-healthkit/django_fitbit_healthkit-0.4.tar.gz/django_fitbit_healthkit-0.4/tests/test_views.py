from django.test import TestCase
from django.urls import reverse

# path("login", views.login, name="fitbitlogin"),
# path("success", views.success, name="fitbitsuccess"),
# path("webhook", views.fitbit_subscription, name="fitbitsubscription"),

class MyViewTest(TestCase):
    def test_my_view(self):
        response = self.client.get(reverse('fitbitlogin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, world!')
