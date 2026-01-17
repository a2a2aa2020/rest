# 🚀 نشر التطبيق الكامل على الإنترنت

## الخطوات البسيطة:

### 1️⃣ **ارفع الملفات الجديدة على GitHub:**

في المتصفح، اذهب إلى:
```
https://github.com/a2a2aa2020/rest
```

اضغط **"Add file"** → **"Upload files"**

ارفع هذين الملفين من مجلد `backend/`:
- `Procfile`
- `runtime.txt`

---

### 2️⃣ **سجّل حساب على Render.com:**

1. اذهب إلى: https://render.com
2. اضغط **"Get Started for Free"**
3. سجّل باستخدام **GitHub account**

---

### 3️⃣ **أنشئ Web Service جديد:**

1. في Dashboard، اضغط **"New +"** → **"Web Service"**
2. اختر repository: **"rest"**
3. املأ المعلومات:
   - **Name:** `restaurant-inspection-api`
   - **Region:** اختر الأقرب لك
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Instance Type:** اختر **Free**
5. اضغط **"Create Web Service"**

---

### 4️⃣ **انتظر النشر (5-10 دقائق):**

Render سيقوم بـ:
- تحميل الكود
- تثبيت المكتبات
- تشغيل Backend

---

### 5️⃣ **احصل على الرابط:**

بعد النشر الناجح، ستحصل على رابط مثل:
```
https://restaurant-inspection-api.onrender.com
```

---

### 6️⃣ **حدّث Frontend:**

في ملف `frontend/js/inspection.js`، غيّر:
```javascript
// من:
fetch('http://localhost:8001/api/inspect', ...)

// إلى:
fetch('https://restaurant-inspection-api.onrender.com/api/inspect', ...)
```

افعل نفس الشيء في `frontend/js/results.js`

---

### 7️⃣ **ارفع Frontend على GitHub Pages:**

1. في repository settings → Pages
2. Source: `main` branch
3. Folder: `/`
4. Save

---

### 8️⃣ **الرابط النهائي:**

افتح على الموبايل:
```
https://a2a2aa2020.github.io/rest/frontend/index.html
```

---

## ✅ **النتيجة:**

- Backend يعمل على Render.com
- Frontend يعمل على GitHub Pages
- يمكنك فتحه من أي موبايل أو جهاز!

---

## 💡 **ملاحظة مهمة:**

Render المجاني قد يأخذ 30-60 ثانية للتشغيل في أول استخدام (لأنه ينام بعد عدم الاستخدام).
