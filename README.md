# VetCare - Online Veterinary Appointment System

A modern, full-featured web application for veterinary clinics, pet owners, and hospital administrators. Built with Python & Django, styled with a clean healthcare aesthetic inspired by modern medical UI design principles (light blue background, large white rounded surfaces, black pill action buttons, and responsive animal healthcare components).

---

## 🐾 Technology Stack

- **Backend Framework:** Django (Python 3.11 / 3.12 / 3.14)
- **Database:** SQLite (default for local development) / PostgreSQL (recommended & auto-configured for Render production via `dj-database-url`)
- **Static Assets Serving:** WhiteNoise with compressed manifest storage
- **WSGI Production Server:** Gunicorn
- **Frontend:** Responsive HTML5, Vanilla Modern CSS System with CSS Custom Properties, Google Fonts (*Plus Jakarta Sans*), and lightweight SVG vector assets

---

## 🎨 Visual Identity & Theme Highlights

- **Background:** Soft sky blue (`#D9F0FA`) with subtle ambient organic curves.
- **Card Surfaces:** High-contrast white containers (`#FFFFFF`) with generous border radius (`32px`) and gentle elevation shadows.
- **Color Accents:** Primary medical blue (`#79B9D8`), vibrant cyan (`#21B8C8`), deep charcoal (`#101820`).
- **Pill Buttons:** Minimalist black pill buttons (`#05090B`) with subtle hover elevation.
- **Hero Section:** Sky blue rounded banner featuring high-resolution animal portraiture, concentric circular line art, and floating feature badges (*Own laboratory*, *24/7 animal assistance*, *Narrow-profile specialists*, *High-tech equipment*).

---

## 🚀 Key Features

### Public Portal
- **Homepage (`/`):** Hero section, departments showcase, specialized care programs, 3-step booking explainer, emergency contacts.
- **About Us (`/about_us/`):** Hospital history (since 2014), facility statistics, medical categories overview.
- **Services (`/services/`):** Full catalog of clinical treatments and procedures with direct booking buttons.
- **Category Details (`/category/<category_name>/`):** Specialized care modules (Wildlife, Emergency, Rehabilitation, Exotic Pets, Consulting, etc.).
- **Contact & Feedback (`/contact/`):** Inquiry submission form with real-time CSRF protection, Google Maps clinic location, emergency phone pill.

### Pet Owner Portal
- **Authentication (`/login/`, `/register/`):** Role-based sign-in and registration with input validations.
- **User Dashboard (`/dashboard/`):** Real-time booking metrics (Total, Approved, Pending, Completed), profile summary, and recent visit log.
- **Book Appointment (`/create_appointment/`):** Multi-step form with service selector, pet name/breed, date validation (past dates blocked), time slot selection, and duplicate booking prevention.
- **My Appointments (`/appointments/`):** Complete appointment history with color-coded status badges (*Approved*, *Pending*, *Rejected*) and clinical progress (*Completed*, *In Progress*).
- **Edit Profile (`/edit-profile/`):** Account information and password management.

### Administration Command Center
- **Admin Dashboard (`/admin-dashboard/`):** Live operational KPI widgets for pending reviews, approved appointments, completed care, client inquiries, and user accounts.
- **Pending Review (`/admin-pending/`):** Triage workflow to review and approve or decline incoming requests with automatic email notification dispatch.
- **Active Appointments (`/admin-appointments/`):** Management of approved visits with direct *Mark Work Done* completion action.
- **Completed Archive (`/completed-appointments/`):** Historical archive of concluded pet visits.
- **Rejected Archive (`/admin-cancelled/`):** Log of declined appointments.
- **Customer Messages (`/admin-feedback/`):** Complete feedback table with inspection, email replies (`/view-contact/<id>/`), and deletion.
- **Service Management (`/add-service/`):** Form to publish new medical services with title, description, and photo upload.
- **User Management (`/admin-users/`, `/edit-user/<id>/`):** Directory of client accounts with editing and removal controls.

---

## 💻 Local Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd vetcare
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy the template `.env.example` to `.env`:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```
Edit `.env` to suit your local setup (defaults work out-of-the-box with SQLite).

### 5. Run database migrations
```bash
python manage.py migrate
```

### 6. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 7. Run automated test suite
```bash
python manage.py test
```

### 8. Start local development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🌐 Deploying to Render

This project is fully pre-configured for zero-friction Render deployment using `render.yaml` or manual Web Service creation.

### Option A: Blueprint Deployment (Recommended)
1. Push your repository to GitHub or GitLab.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New +** &rarr; **Blueprint**.
3. Select your repository. Render will automatically detect `render.yaml`.
4. Click **Apply**. Render will run `build.sh` and deploy your web service!

### Option B: Manual Web Service Setup
1. In the [Render Dashboard](https://dashboard.render.com/), click **New +** &rarr; **Web Service**.
2. Connect your GitHub/GitLab repository.
3. Choose **Python** as the runtime.
4. Set the following fields:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn vetcare.wsgi:application`
5. Under **Environment Variables**, configure the following:

| Variable | Value / Description |
|---|---|
| `PYTHON_VERSION` | `3.11.9` |
| `DEBUG` | `False` |
| `SECRET_KEY` | *(Click "Generate" or paste a strong random key)* |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` |
| `DATABASE_URL` | *(Optional: paste PostgreSQL external URL or connect Render PostgreSQL)* |
| `EMAIL_HOST_USER` | *(Optional: your clinic email for outgoing notifications)* |
| `EMAIL_HOST_PASSWORD` | *(Optional: Google App Password for Gmail SMTP)* |

---

## 🛡️ Security & Production Best Practices

- **Debug Mode:** Always disabled (`DEBUG=False`) in production environments.
- **Secrets Management:** Sensitive keys and database URLs are loaded from environment variables and never committed to version control.
- **CSRF Protection:** Enabled on all forms with trusted origins configured for Render.
- **Static Asset Caching:** Handled by WhiteNoise with compressed file hashes (`CompressedManifestStaticFilesStorage`).
- **Resilient Emailing:** Email notifications are guarded so network issues never block patient approvals or client actions.
