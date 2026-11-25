import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="案件名稱")),
                ("client_name", models.CharField(max_length=100, verbose_name="客戶名稱")),
                ("budget", models.PositiveIntegerField(default=0, verbose_name="預算（元）")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("negotiating", "洽談中"),
                            ("in_progress", "進行中"),
                            ("done", "已完成"),
                        ],
                        default="negotiating",
                        max_length=20,
                        verbose_name="狀態",
                    ),
                ),
                ("deadline", models.DateField(blank=True, null=True, verbose_name="截止日")),
                ("note", models.TextField(blank=True, verbose_name="備註")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="建立時間")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="建立者",
                    ),
                ),
            ],
            options={
                "verbose_name": "案件",
                "verbose_name_plural": "案件",
                "ordering": ["-updated_at"],
            },
        ),
    ]
