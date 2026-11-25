from django.contrib import admin
from django.utils.html import format_html

from .models import Project

admin.site.site_header = "接案管理後台"
admin.site.site_title = "接案管理後台"
admin.site.index_title = "總覽"
admin.site.site_url = "/"

STATUS_COLORS = {
    Project.Status.NEGOTIATING: ("#64748b", "#f1f5f9"),
    Project.Status.IN_PROGRESS: ("#2563eb", "#dbeafe"),
    Project.Status.DONE: ("#059669", "#d1fae5"),
}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client_name", "budget_display", "status_badge", "deadline", "owner", "updated_at")
    list_display_links = ("title",)
    list_filter = ("status", "deadline", "owner")
    search_fields = ("title", "client_name", "note")
    date_hierarchy = "created_at"
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")
    actions = ("mark_in_progress", "mark_done")
    fieldsets = (
        ("案件資訊", {"fields": ("title", "client_name", "owner")}),
        ("金額與進度", {"fields": ("budget", "status", "deadline")}),
        ("備註", {"fields": ("note",)}),
        ("紀錄", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="預算", ordering="budget")
    def budget_display(self, obj):
        return f"${obj.budget:,}"

    @admin.display(description="狀態", ordering="status")
    def status_badge(self, obj):
        fg, bg = STATUS_COLORS.get(obj.status, ("#334155", "#e2e8f0"))
        return format_html(
            '<span class="status-pill" style="color:{};background:{}">{}</span>',
            fg,
            bg,
            obj.get_status_display(),
        )

    @admin.action(description="標記為「進行中」")
    def mark_in_progress(self, request, queryset):
        n = queryset.update(status=Project.Status.IN_PROGRESS)
        self.message_user(request, f"已將 {n} 筆案件標記為進行中。")

    @admin.action(description="標記為「已完成」")
    def mark_done(self, request, queryset):
        n = queryset.update(status=Project.Status.DONE)
        self.message_user(request, f"已將 {n} 筆案件標記為已完成。")
