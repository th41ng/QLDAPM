# ⚡ Deploy Nhanh (5 phút)

## Backend → Fly.io

```bash
# 1. Cài Fly CLI
# Windows: iwr https://fly.io/install.ps1 -useb | iex
# Mac/Linux: curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Launch app
fly launch
# → Chọn: sin region, N cho database, Y cho Dockerfile

# 4. Set secrets (sửa giá trị thực tế)
fly secrets set DATABASE_URL="mysql+pymysql://user:pass@host/db"
fly secrets set SECRET_KEY="your-secret-key"
fly secrets set JWT_SECRET_KEY="your-jwt-secret"
fly secrets set MAIL_USERNAME="your-email@gmail.com"
fly secrets set MAIL_PASSWORD="your-app-password"

# 5. Deploy
fly deploy

# ✅ Backend chạy tại: https://qlda-backend.fly.dev/api
```

## Frontend → Vercel

```bash
# 1. Cài Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
cd frontend
vercel --prod

# 4. Add environment variable
# Vào https://vercel.com → project → settings → environment variables
# Thêm: VITE_API_BASE_URL = https://qlda-backend.fly.dev/api

# 5. Redeploy
vercel --prod

# ✅ Frontend chạy tại: https://qlda-frontend.vercel.app
```

## Test

```bash
curl https://qlda-backend.fly.dev/healthz
# Kết quả: {"status":"ok"}
```

---

**Xong!** Truy cập https://qlda-frontend.vercel.app

Nếu gặp issue, xem [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) để chi tiết.
