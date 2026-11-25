from django import template
from django.db.models import Count, Q, Sum

from projects.models import Project

register = template.Library()


@register.simple_tag
def project_stats():
    """後台首頁統計卡片用的數字（所有使用者的案件）。"""
    s = Project.objects.aggregate(
        total=Count("id"),
        negotiating=Count("id", filter=Q(status=Project.Status.NEGOTIATING)),
        in_progress=Count("id", filter=Q(status=Project.Status.IN_PROGRESS)),
        done=Count("id", filter=Q(status=Project.Status.DONE)),
        done_budget=Sum("budget", filter=Q(status=Project.Status.DONE)),
        pipeline_budget=Sum("budget", filter=~Q(status=Project.Status.DONE)),
    )
    s["done_budget"] = s["done_budget"] or 0
    s["pipeline_budget"] = s["pipeline_budget"] or 0
    s["recent"] = Project.objects.select_related("owner")[:5]
    return s
