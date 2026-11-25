from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Project

User = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pass-12345-x")
        self.bob = User.objects.create_user("bob", password="pass-12345-x")
        self.alice_project = Project.objects.create(
            owner=self.alice, title="LINE 預約系統", client_name="小美髮廊", budget=30000
        )

    def test_login_required(self):
        resp = self.client.get(reverse("project_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp.url)

    def test_user_sees_only_own_projects(self):
        self.client.login(username="bob", password="pass-12345-x")
        resp = self.client.get(reverse("project_list"))
        self.assertNotContains(resp, "LINE 預約系統")

    def test_cannot_edit_others_project(self):
        self.client.login(username="bob", password="pass-12345-x")
        url = reverse("project_update", args=[self.alice_project.pk])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_create_project_sets_owner(self):
        self.client.login(username="alice", password="pass-12345-x")
        resp = self.client.post(
            reverse("project_create"),
            {
                "title": "爬蟲",
                "client_name": "某公司",
                "budget": 8000,
                "status": "in_progress",
                "deadline": "",
                "note": "",
            },
        )
        self.assertRedirects(resp, reverse("project_list"))
        self.assertEqual(Project.objects.get(title="爬蟲").owner, self.alice)

    def test_search_and_filter(self):
        Project.objects.create(owner=self.alice, title="官網", client_name="咖啡店", status="done")
        self.client.login(username="alice", password="pass-12345-x")
        resp = self.client.get(reverse("project_list"), {"q": "咖啡"})
        self.assertContains(resp, "官網")
        self.assertNotContains(resp, "LINE 預約系統")
        resp = self.client.get(reverse("project_list"), {"status": "done"})
        self.assertContains(resp, "官網")
        self.assertNotContains(resp, "LINE 預約系統")

    @override_settings(
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        }
    )
    def test_admin_dashboard_and_changelist(self):
        User.objects.create_superuser("admin", password="pass-12345-x")
        self.client.login(username="admin", password="pass-12345-x")
        resp = self.client.get(reverse("admin:index"))
        self.assertContains(resp, "接案管理後台")
        self.assertContains(resp, "已完成收入")
        self.assertContains(resp, "LINE 預約系統")
        resp = self.client.get(reverse("admin:projects_project_changelist"))
        self.assertContains(resp, "$30,000")
        self.assertContains(resp, "status-pill")

    def test_delete_project(self):
        self.client.login(username="alice", password="pass-12345-x")
        resp = self.client.post(reverse("project_delete", args=[self.alice_project.pk]))
        self.assertRedirects(resp, reverse("project_list"))
        self.assertFalse(Project.objects.exists())
