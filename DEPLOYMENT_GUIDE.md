# 🚀 Hướng dẫn Deploy QLDA

## Tổng quan
- **Backend**: Fly.io (hoặc Heroku backup)
- **Frontend**: Vercel
- **Database**: MySQL (tự cấu hình hoặc dùng ngoài)

---

## 📋 Yêu cầu trước khi deploy

1. **GitHub account** (để liên kết với Vercel/Fly)
2. **Fly.io account** (miễn phí): https://fly.io
3. **Vercel account** (miễn phí): https://vercel.com
4. **Git CLI** + **Node.js** + **Python 3.11+**

---

## 🔧 Bước 1: Chuẩn bị repo

### 1.1 Push code lên GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/qlda.git
git branch -M main
git push -u origin main
```

### 1.2 Tạo file `.env` production (lưu ý: không commit `.env`)
```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin thực tế
```

---

## ⚙️ Bước 2: Deploy Backend lên Fly.io

### 2.1 Cài đặt Fly CLI
```bash
# Windows (PowerShell):
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux:
curl -L https://fly.io/install.sh | sh
```

### 2.2 Login vào Fly
```bash
fly auth login
# Truy cập link, đăng nhập, copy token
```

### 2.3 Tạo app Fly
```bash
cd /path/to/qlda  # Thư mục root repo
fly launch
```

Khi được hỏi:
- App name: `qlda-backend` (hoặc tên khác)
- Region: `sin` (Singapore, gần Việt Nam)
- Database: `N` (dùng ngoài)
- Build with Dockerfile: `Y`

### 2.4 Thiết lập biến môi trường
```bash
fly secrets set DATABASE_URL="mysql+pymysql://user:pass@host/dbname"
fly secrets set SECRET_KEY="your-secret-key-here"
fly secrets set JWT_SECRET_KEY="your-jwt-secret-key-here"
fly secrets set MAIL_SERVER="smtp.gmail.com"
fly secrets set MAIL_PORT="587"
fly secrets set MAIL_USE_TLS="true"
fly secrets set MAIL_USERNAME="your-email@gmail.com"
fly secrets set MAIL_PASSWORD="your-app-password"
fly secrets set CLOUDINARY_CLOUD_NAME="your-cloud-name"
fly secrets set CLOUDINARY_API_KEY="your-api-key"
fly secrets set CLOUDINARY_API_SECRET="your-api-secret"
```

### 2.5 Deploy
```bash
fly deploy
```

Backend của bạn sẽ chạy tại: `https://qlda-backend.fly.dev/api`

### 2.6 Kiểm tra health
```bash
curl https://qlda-backend.fly.dev/healthz
# Kết quả: {"status":"ok"}
```

---

## 🎨 Bước 3: Deploy Frontend lên Vercel

### 3.1 Cài Vercel CLI
```bash
npm install -g vercel
```

### 3.2 Login vào Vercel
```bash
vercel login
# Chọn GitHub account
```

### 3.3 Deploy
```bash
cd frontend
vercel --prod
```

Khi được hỏi:
- Project name: `qlda-frontend` (hoặc tên khác)
- Link to existing project: `N`

### 3.4 Thêm Environment Variables
Vào https://vercel.com → Project → Settings → Environment Variables

Thêm:
```
VITE_API_BASE_URL = https://qlda-backend.fly.dev/api
```

### 3.5 Redeploy
```bash
vercel --prod
```

Frontend của bạn sẽ chạy tại: `https://qlda-frontend.vercel.app`

---

## 🔗 Bước 4: Cấu hình CORS (Backend)

Backend đã được cấu hình hỗ trợ:
- `https://*.vercel.app` (tất cả Vercel)
- `https://*.netlify.app` (tất cả Netlify)
- Localhost (dev)

Không cần sửa gì thêm nếu dùng Vercel ✅

---

## 🗄️ Bước 5: Cấu hình Database

### Tùy chọn A: Sử dụng MySQL ngoài (AWS RDS, PlanetScale, etc)
```
DATABASE_URL=mysql+pymysql://user:pass@your-host.com/dbname
```

### Tùy chọn B: Deploy MySQL riêng
```bash
# Ví dụ: PlanetScale (MySQL as a Service)
# 1. Tạo account https://planetscale.com
# 2. Tạo database
# 3. Copy connection string
# 4. Set DATABASE_URL trên Fly
fly secrets set DATABASE_URL="mysql+pymysql://..."
```

---

## 📧 Bước 6: Cấu hình Email (Gmail)

### 6.1 Bật 2FA trên Gmail
- https://myaccount.google.com/security

### 6.2 Tạo App Password
- https://myaccount.google.com/apppasswords
- Chọn: Mail → Windows Computer
- Copy password (16 ký tự)

### 6.3 Set trên Fly
```bash
fly secrets set MAIL_USERNAME="your-email@gmail.com"
fly secrets set MAIL_PASSWORD="xxxxxxxx xxxx xxxx xxxx"  # 16 ký tự
```

---

## ☁️ Bước 7: Cấu hình Cloudinary (Upload ảnh)

### 7.1 Tạo account
- https://cloudinary.com

### 7.2 Lấy API keys
- Dashboard → Settings → API

### 7.3 Set trên Fly
```bash
fly secrets set CLOUDINARY_CLOUD_NAME="your-name"
fly secrets set CLOUDINARY_API_KEY="your-key"
fly secrets set CLOUDINARY_API_SECRET="your-secret"
```

---

## 🧪 Bước 8: Test

### Test Backend
```bash
curl https://qlda-backend.fly.dev/healthz
curl https://qlda-backend.fly.dev/api/auth/me
```

### Test Frontend
Truy cập: https://qlda-frontend.vercel.app

Kiểm tra:
- [ ] Trang login hiển thị
- [ ] F12 → Network → request tới `/api/` không bị CORS error
- [ ] Có thể submit form

---

## 🔄 Cập nhật sau này

### Update Backend
```bash
git add .
git commit -m "Fix: something"
git push origin main
fly deploy
```

### Update Frontend
```bash
git add .
git commit -m "Feat: something"
git push origin main
# Vercel tự động deploy
```

---

## 🆘 Troubleshooting

### Backend timed out khi deploy
→ Tắt `EMBEDDING_WARMUP_ON_START` (đã tắt sẵn trong config)

### Frontend CORS error
→ Kiểm tra VITE_API_BASE_URL trên Vercel Environment Variables

### Database connection error
→ Kiểm tra DATABASE_URL có đúng format
→ Test kết nối local trước: `flask shell`

### Email không gửi được
→ Bật 2FA Gmail, tạo App Password
→ Kiểm tra MAIL_USERNAME/MAIL_PASSWORD trên Fly

---

## 📊 Chi phí ước tính

| Dịch vụ | Free tier | Chi phí |
|--------|-----------|--------|
| Fly.io (Backend) | 3 shared-cpu-1x 256MB | $0/tháng |
| Vercel (Frontend) | ∞ deployments, 100GB bandwidth | $0/tháng |
| PlanetScale (MySQL) | 5GB data, 1B rows | $0/tháng |
| Cloudinary (CDN) | 25 credits/tháng | $0/tháng (hoặc trả thêm) |
| **TỔNG** | | **$0/tháng** |

Sau khi vượt free tier, chi phí sẽ tăng.

---

## ✅ Checklist Deploy

- [ ] Repo đã push lên GitHub
- [ ] Backend đã deploy lên Fly
- [ ] Frontend đã deploy lên Vercel
- [ ] Environment variables đã set
- [ ] Database đã kết nối
- [ ] Email đã test gửi
- [ ] CORS không lỗi
- [ ] Healthz endpoint trả về 200

---

## 🎉 Hoàn tất!

App của bạn bây giờ chạy trên:
- **Frontend**: https://qlda-frontend.vercel.app
- **Backend**: https://qlda-backend.fly.dev/api

Chia sẻ link cho bạn bè!
