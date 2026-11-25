from django.conf import settings
from django.db import models
from django.urls import reverse


class Project(models.Model):
    class Status(models.TextChoices):
        NEGOTIATING = "negotiating", "洽談中"
        IN_PROGRESS = "in_progress", "進行中"
        DONE = "done", "已完成"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="建立者",
    )
    title = models.CharField("案件名稱", max_length=100)
    client_name = models.CharField("客戶名稱", max_length=100)
    budget = models.PositiveIntegerField("預算（元）", default=0)
    status = models.CharField(
        "狀態", max_length=20, choices=Status.choices, default=Status.NEGOTIATING
    )
    deadline = models.DateField("截止日", null=True, blank=True)
    note = models.TextField("備註", blank=True)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "案件"
        verbose_name_plural = "案件"

    def __str__(self):
        return f"{self.title}（{self.client_name}）"

    def get_absolute_url(self):
        return reverse("project_list")
