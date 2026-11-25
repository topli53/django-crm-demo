# 接案管理 Demo（Django）

用 Django 寫的小型案件管理系統。示範會員系統、資料 CRUD、搜尋篩選、管理後台、部署，都是接案常見的需求。

## 功能

- 註冊、登入、登出（Django 內建認證）
- 案件的新增、查詢、修改、刪除，每個使用者只看得到自己的資料
- 依案件名稱或客戶搜尋，依狀態篩選，分頁
- 統計卡片：案件數、進行中、已完成收入、洽談中＋進行中的金額
- Django Admin 後台：搜尋、篩選，可以直接在列表改狀態
- 單元測試：權限隔離、CRUD、搜尋篩選
- Docker 部署（gunicorn＋whitenoise）

## 本機執行

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # 建立後台帳號
python manage.py runserver
```

打開 http://127.0.0.1:8000 註冊帳號；後台在 http://127.0.0.1:8000/admin/

## 測試

```bash
python manage.py test
```

## 部署（以 Render 為例）

1. 推到 GitHub。
2. 在 Render 新增 Web Service，選這個 repo，Runtime 選 Docker。
3. 設定環境變數：
   - `DJANGO_SECRET_KEY`：一串隨機長字串
   - `DJANGO_ALLOWED_HOSTS`：`你的服務名稱.onrender.com`
   - `DJANGO_CSRF_TRUSTED_ORIGINS`：`https://你的服務名稱.onrender.com`
4. 部署完成後就有公開網址，可以放進提案。

> 這個 Demo 用 SQLite，免費方案重新部署時資料會被清掉。正式專案改成 PostgreSQL。

## 技術

Python 3.12 · Django 5.2 · Bootstrap 5 · SQLite · Docker · gunicorn · whitenoise
