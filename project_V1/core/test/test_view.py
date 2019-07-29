from django.test import TestCase,Client
from django.urls import reverse
#from core.models import following,tweets_data,notification_data
import json

# class TestCoreViews(TestCase):

#     def test_addfriend(self):

#         client=Client()
#         response=client.get(reverse("addfriend"))

#         self.assertEquals(response.status_code,302)
#         self.assertTemplateUsed(response,"login")