from django.test import Client,TestCase
from taskmanager.models import Task,SubTask
from datetime import datetime
from django.urls import reverse


class URLTests(TestCase):
    client=Client()

    def test_task_creation_view(self):
        response=self.client.get(reverse('taskmanager:task_create'))
        self.assertEqual(response.status_code,200)
        
