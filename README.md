# FastAPI CRUD Starter

## 1) Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 2) Environment

ค่าเริ่มต้นใน `.env.example`:

```env
PORT=3001
NODE_ENV=production
JWT_SECRET=your-secret
CORS_ORIGIN=http://localhost:3000,http://192.168.1.106:3000
DATABASE_URL=postgresql://<user>:<pass>@<host>/<db>?sslmode=require
DB_SCHEMA=users
```

## 3) Run API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
```

## 4) CRUD Endpoints

- `POST /users` สร้าง user
- `GET /users` ดึง list user
- `GET /users/{user_id}` ดึง user รายตัว
- `PATCH /users/{user_id}` แก้ไขชื่อ user
- `DELETE /users/{user_id}` ลบ user

Swagger UI: `http://localhost:3001/docs`