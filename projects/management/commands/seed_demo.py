from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from projects.models import Project

DEMO = [
    ("LINE 預約系統", "小美髮廊", 30000, "in_progress", 14, "LINE Bot 預約、自動提醒、後台排班"),
    ("商品價格爬蟲", "優品電商", 8000, "done", -20, "每日抓取競品價格，輸出 Excel"),
    ("形象官網改版", "日光咖啡", 25000, "done", -45, "RWD 改版、SEO 基本設定"),
    ("ERP 報表模組", "宏達貿易", 45000, "in_progress", 30, "月報、客戶批數統計、匯出 Excel"),
    ("WordPress 網站修復", "青禾設計工作室", 4500, "done", -7, "外掛衝突導致跑版，更新後修正"),
    ("NAS 自動備份＋Telegram 通知", "安心會計事務所", 6000, "negotiating", 21, "每晚備份資料庫並回報結果"),
    ("會員管理後台", "健動健身房", 38000, "negotiating", 40, "會員、課程、儲值紀錄管理"),
    ("網站部署上線", "新創 App 團隊", 5000, "in_progress", 5, "Ubuntu + Nginx + HTTPS"),
]


class Command(BaseCommand):
    help = "建立展示用的範例案件：python manage.py seed_demo <使用者帳號>"

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--reset", action="store_true", help="先刪除該使用者原有的案件")

    def handle(self, username, reset=False, **options):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"找不到使用者「{username}」")

        if reset:
            Project.objects.filter(owner=user).delete()

        today = date.today()
        for title, client, budget, status, days, note in DEMO:
            Project.objects.create(
                owner=user,
                title=title,
                client_name=client,
                budget=budget,
                status=status,
                deadline=today + timedelta(days=days),
                note=note,
            )
        self.stdout.write(self.style.SUCCESS(f"已為 {username} 建立 {len(DEMO)} 筆範例案件"))
