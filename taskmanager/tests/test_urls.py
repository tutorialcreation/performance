from django.test import Client,TestCase
from taskmanager.models import Task,SubTask
from datetime import datetime
from django.urls import reverse


class URLTests(TestCase):
    client=Client()

    def test_index_url(self):
        response=self.client.get(reverse('taskmanager:index'))
        self.assertEqual(response.status_code,200)
    
    def test_chart_deadline_url(self):
        response=self.client.get(reverse('taskmanager:chart_deadline'))
        self.assertEqual(response.status_code,200)
    
    def test_chart_resubmission_url(self):
        response=self.client.get(reverse('taskmanager:chart_resubmission'))
        self.assertEqual(response.status_code,200)

    def test_chart_reset_url(self):
        response=self.client.get(reverse('taskmanager:chart_reset'))
        self.assertEqual(response.status_code,200)

    def test_chart_quality_url(self):
        response=self.client.get(reverse('taskmanager:chart_quality'))
        self.assertEqual(response.status_code,200)
    
    def test_team_detail_url(self):
        response=self.client.get(reverse('taskmanager:team_detail',kwargs={'team_id':1}))
        self.assertEqual(response.status_code,200)
    
    def test_team_details_url(self):
        response=self.client.get(reverse('taskmanager:team_details',kwargs={'team_id':1}))
        self.assertEqual(response.status_code,200)

    def test_team_create_url(self):
        response=self.client.get(reverse('taskmanager:team_create'))
        self.assertEqual(response.status_code,200)

    def test_team_remove_url(self):
        response=self.client.get(reverse('taskmanager:team_remove_member',kwargs={'team_id':team_id}))
        self.assertEqual(response.status_code,200)

    def test_team_add_view_url(self):
        response=self.client.get(reverse('taskmanager:team_add_member',kwargs={'team_id':1}))
        self.assertEqual(response.status_code,200)

    def test_team_delete_url(self):
        response=self.client.get(reverse('taskmanager:team_delete',kwargs={'team_id':1}))
        self.assertEqual(response.status_code,200)

    def test_my_tasks_url(self):
        response=self.client.get(reverse('taskmanager:task_my_tasks'))
        self.assertEqual(response.status_code,200)

    def test_team_tasks_url(self):
        response=self.client.get(reverse('taskmanager:team_tasks',kwargs={'team_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_update_url(self):
        response=self.client.get(reverse('taskmanager:task_update',kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)

    def test_task_rating_url(self):
        response=self.client.get(reverse('taskmanager:task_rating',kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)

    def test_subtask_rating_url(self):
        response=self.client.get(reverse('taskmanager:subtask_rating',kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)

    def test_task_comment_url(self):
        response=self.client.get(reverse('taskmanager:task_comment',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_accept_url(self):
        response=self.client.get(reverse('taskmanager:task_accept',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_resubmit_url(self):
        response=self.client.get(reverse('taskmanager:task_resubmit',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_mark_completed_url(self):
        response=self.client.get(reverse('taskmanager:task_mark_completed',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_mark_pending_approved(self):
        response=self.client.get(reverse('taskmanager:task_mark_pending_approved',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_mark_revision_url(self):
        response=self.client.get(reverse('taskmanager:task_mark_revision',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)

    def test_task_delete_url(self):
        response=self.client.get(reverse('taskmanager:task_delete',kwargs={'task_id':1}))
        self.assertEqual(response.status_code,200)
        
    def test_task_create_url(self):
        response=self.client.get(reverse('taskmanager:task_create'))
        self.assertEqual(response.status_code,200)

    def test_task_search_url(self):
        response=self.client.get(reverse('taskmanager:task_search'))
        self.assertEqual(response.status_code,200)

    def test_signup_url(self):
        response=self.client.get(reverse('taskmanager:signup'))
        self.assertEqual(response.status_code,200)

    def test_load_members_url(self):
        response=self.client.get(reverse('taskmanager:ajax_load_members'))
        self.assertEqual(response.status_code,200)

    def test_load_projects_url(self):
        response=self.client.get(reverse('taskmanager:ajax_load_projects'))
        self.assertEqual(response.status_code,200)
