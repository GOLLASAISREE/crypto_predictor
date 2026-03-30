# 🚀 CryptoPredictor AI — Django ML Project

## 📋 Project Overview
A full-stack Django web application for cryptocurrency price prediction using 4 ML algorithms:
- **Linear Regression** — Trend-based prediction
- **LSTM** (Long Short-Term Memory) — Deep learning time series
- **SVM** (Support Vector Machine) — High-dimensional classification
- **Random Forest** — Ensemble learning

---

## 🛠️ Software Requirements
| Component | Requirement |
|-----------|-------------|
| OS | Windows 10 / 11 |
| Python | 3.9 or higher |
| Framework | Django 4.2.x |
| Database | SQLite (built-in) |
| Frontend | HTML, CSS, JavaScript, Bootstrap 5 |

---

## ⚡ Quick Setup (Step by Step)

### Step 1 — Install Python 3.9+
Download from: https://www.python.org/downloads/

### Step 2 — Open Terminal / Command Prompt
```
cd path\to\crypto_predictor
```

### Step 3 — Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run Auto Setup (creates DB + admin user)
```bash
python setup.py
```

### Step 6 — Start the Server
```bash
python manage.py runserver
```

### Step 7 — Open Browser
```
http://127.0.0.1:8000/
```

---

## 🔑 Login Credentials

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | `admin`  | `admin123` |
| User  | `demo`   | `demo123`  |

---

## 📁 Project Structure
```
crypto_predictor/
├── manage.py                    # Django management
├── setup.py                     # Auto-setup script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database (auto-created)
│
├── crypto_predictor/            # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── crypto_app/                  # Main application
    ├── models.py                # Database models
    ├── views.py                 # All view logic
    ├── urls.py                  # URL routing
    ├── forms.py                 # Django forms
    ├── ml_engine.py             # 🤖 ALL ML algorithms
    ├── admin.py                 # Django admin config
    │
    ├── templates/crypto_app/
    │   ├── base.html            # Base layout
    │   ├── home.html            # 🏠 Homepage (Bitcoin logo)
    │   ├── login.html           # 👤 User login
    │   ├── admin_login.html     # 🔐 Admin login
    │   ├── register.html        # 📝 Registration
    │   ├── dashboard.html       # 📊 User dashboard
    │   ├── prediction_result.html  # 📈 ML Results
    │   ├── prediction_history.html # 🕐 History
    │   ├── admin_dashboard.html    # ⚙️ Admin panel
    │   ├── manage_users.html       # 👥 User management
    │   ├── edit_user.html          # ✏️ Edit user
    │   ├── admin_predictions.html  # 📋 All predictions
    │   └── contact.html            # 📧 Contact
    │
    └── migrations/              # DB migrations
```

---

## 🧠 ML Algorithms Used

### 1. Linear Regression (`lr`)
- Features: MA7, MA21, MA30, RSI, price change, volatility, lag features
- Scaled with StandardScaler
- 80/20 train-test split

### 2. LSTM — Long Short-Term Memory (`lstm`)
- 60-day sequence length
- MinMax scaled data
- Captures long-term temporal dependencies

### 3. Support Vector Machine (`svm`)
- RBF kernel (C=100, gamma=0.1)
- StandardScaler preprocessing
- 8 technical indicator features

### 4. Random Forest (`rf`)
- 200 estimators, max_depth=10
- 12 feature inputs
- Feature importance visualization

---

## 📊 Output Screens

1. **Home Page** — Bitcoin logo, animated hero, live ticker
2. **User Login** — Clean login form
3. **Admin Login** — Separate admin portal
4. **Register** — User registration
5. **Dashboard** — Crypto + algorithm selector + date picker
6. **Prediction Result** — Price chart, ML metrics, investment advice
7. **Prediction History** — Table of all past predictions
8. **Admin Dashboard** — Stats, recent users, recent predictions
9. **Manage Users** — Edit/activate/deactivate/delete users
10. **All Predictions** — Admin view of every prediction

---

## 💡 Investment Suggestions
Based on predicted price change %:
- `> +15%` → **STRONG BUY 🚀**
- `+5% to +15%` → **BUY 📈**
- `0% to +5%` → **HOLD / WATCH 👀**
- `-5% to 0%` → **CAUTION ⚠️**
- `< -5%` → **AVOID / SELL 📉**

---

## ⚠️ Disclaimer
This application is for **educational purposes only**. Not financial advice.

---

## ☁️ Deploy on Vercel (Git-based)

Vercel is workable for this Django project, but you must use an external Postgres database (SQLite is local-only).

### 1. Import Repository in Vercel
- Go to Vercel dashboard → **Add New...** → **Project**
- Select repo: `GOLLASAISREE/crypto_predictor`
- Keep defaults and deploy

### 2. Add Environment Variables in Vercel Project Settings
- `SECRET_KEY` = any long random string
- `DEBUG` = `False`
- `DATABASE_URL` = your hosted Postgres connection URL
- `ALLOWED_HOSTS` = `.vercel.app`
- `CSRF_TRUSTED_ORIGINS` = `https://*.vercel.app`

### 3. Redeploy
- Trigger a redeploy after setting env vars.

### 4. Run Migrations (one-time)
- Use Vercel CLI or a temporary local command against the same `DATABASE_URL`:
```bash
python manage.py migrate
```

### Notes
- Netlify is not recommended for this full Django app.
- This repo already includes `vercel.json` for routing to Django WSGI.
