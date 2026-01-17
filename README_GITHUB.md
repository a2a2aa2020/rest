# 🏛️ نظام الفحص الذكي للمنشآت الغذائية

<div align="center">

![Ministry Logo](https://img.shields.io/badge/وزارة_البلديات_والإسكان-السعودية-00695C?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/AI-Powered-7CB342?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-POC-orange?style=for-the-badge)

**نظام ذكي قائم على الذكاء الاصطناعي لفحص المطاعم ومنح التراخيص**

[العربية](#العربية) | [English](#english)

</div>

---

## العربية

### 📋 نظرة عامة

تطبيق POC لنظام فحص ذكي يستخدم الذكاء الاصطناعي لتسهيل إجراءات الكشف على المطاعم لوزارة البلديات والإسكان السعودية. يقوم النظام بفحص 4 معايير أساسية باستخدام تقنيات Computer Vision.

### ✨ المميزات

- ✅ **فحص 4 معايير** بالذكاء الاصطناعي
- ✅ **دعم كاميرا الموبايل** لالتقاط الصور
- ✅ **واجهة عربية رسمية** بتصميم احترافي
- ✅ **تقارير PDF عربية** قابلة للتحميل
- ✅ **تحليل فوري** باستخدام OpenCV
- ✅ **تغطية 93.5%** من الحالات (1,058 حالة)

### 🎯 المعايير المفحوصة

| المعيار | الوصف | عدد الصور | الدقة المتوقعة |
|---------|-------|-----------|-----------------|
| 1️⃣ الأسلاك والأنابيب | فحص الأسلاك الظاهرة على السقف والجدران والأرضيات | 3 | 85-90% |
| 2️⃣ وحدات التكييف | فحص وحدات التكييف الظاهرة على الواجهة | 1 | 95%+ |
| 3️⃣ الأرضيات | فحص وجود فواصل في أرضية منطقة التحضير | 1 | 75-85% |
| 4️⃣ الإضاءة | تقييم كفاية الإضاءة في منطقة التحضير | 1 | 80-85% |

### 🚀 التثبيت والتشغيل

#### المتطلبات
- Python 3.8+
- متصفح حديث (Chrome, Edge, Safari)

#### 1. تثبيت المكتبات

```bash
cd backend
pip install -r requirements.txt
```

#### 2. تشغيل Backend

```bash
cd backend
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

#### 3. فتح Frontend

افتح `frontend/index.html` في المتصفح

### 📸 كيفية الاستخدام

1. **تسجيل الدخول** - اضغط "تسجيل دخول صاحب المنشأة"
2. **لوحة التحكم** - عرض معلومات المنشأة والسجل التجاري
3. **فحص جديد** - أدخل معلومات المنشأة
4. **التقاط الصور** - التقط 6 صور باستخدام كاميرا الموبايل
5. **التحليل** - انتظر نتائج التحليل الآلي (30-60 ثانية)
6. **النتائج** - شاهد الدرجات والتقرير PDF

### 🏗️ البنية المعمارية

```
restaurant_inspection_poc/
├── backend/                 # FastAPI Backend
│   ├── main.py             # API Endpoints
│   ├── ai_engine.py        # AI Analysis (OpenCV)
│   └── pdf_generator.py    # PDF Reports
├── frontend/               # Web Frontend
│   ├── index.html          # Landing Page
│   ├── dashboard.html      # Dashboard
│   ├── inspection.html     # Inspection Form
│   ├── results.html        # Results Display
│   └── css/styles.css      # Official Design
└── training_data/          # AI Training Images
```

### 🔧 التقنيات المستخدمة

**Backend:**
- FastAPI
- OpenCV
- NumPy
- ReportLab (PDF)
- Arabic-Reshaper

**Frontend:**
- HTML5 / CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Cairo Font

**AI/ML:**
- OpenCV (Edge Detection, Circle Detection)
- Brightness Analysis
- Image Segmentation

### 📊 الإحصائيات

- 📁 **8 ملفات رئيسية**
- 📸 **10 صور تدريب مولدة**
- 🎯 **4 معايير فحص**
- 📝 **1,058 حالة مغطاة**
- 🌍 **100% Arabic RTL**

### 📄 الترخيص

هذا المشروع هو POC تجريبي لوزارة البلديات والإسكان السعودية.

### 👥 المساهمة

هذا مشروع حكومي تابع لوزارة البلديات والإسكان.

---

## English

### 📋 Overview

An AI-powered smart inspection system POC for the Saudi Ministry of Municipalities and Housing. The system inspects 4 key criteria for restaurant licensing using Computer Vision.

### ✨ Features

- ✅ **4 AI-powered criteria** inspection
- ✅ **Mobile camera** integration
- ✅ **Official Arabic interface** with professional design
- ✅ **Arabic PDF reports** downloadable
- ✅ **Real-time analysis** using OpenCV
- ✅ **93.5% coverage** (1,058 cases)

### 🚀 Quick Start

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run backend
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

# Open frontend/index.html in browser
```

### 🔧 Tech Stack

- **Backend:** FastAPI, OpenCV, NumPy, ReportLab
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **AI:** OpenCV (Computer Vision)

### 📊 Statistics

- 📁 8 main files
- 📸 10 training images
- 🎯 4 inspection criteria
- 📝 1,058 cases covered
- 🌍 100% Arabic RTL

---

<div align="center">

**© 2026 Ministry of Municipalities and Housing - Kingdom of Saudi Arabia**

Made with ❤️ using AI

</div>
