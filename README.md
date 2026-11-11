# VETNEST — Online Veterinary Appointment System

A premium, full-featured web application for veterinary clinics, pet owners, and hospital administrators. Built with Python & Django, redesigned to match the **VETNEST** website design with warm beige backgrounds, cream content containers, elegant Playfair Display serif typography, orange pill-shaped action buttons with circular arrow indicators, and authentic animal photography.

---

## 🐾 Visual Identity & Design System

- **Page Background:** Warm beige (`#E8DCC0`) with subtle decorative paw watermark.
- **Content Container:** Master cream container (`#F6EEDF`) with generous rounded corners (`36px`) and thin white borders (`rgba(255, 255, 255, 0.85)`).
- **Cards & Surfaces:** Warm white/ivory (`#FFFDF8` / `#FFFFFF`) with subtle borders (`#E8DFCF`).
- **Typography:**
  - **Headings:** Elegant serif (*Playfair Display*)
  - **Body / Interface:** Modern clean sans-serif (*Plus Jakarta Sans*)
- **Buttons:** Signature VETNEST orange pill buttons (`#FFB323`) with circular black arrow icons (`->`).
- **Photography Assets:**
  - `dog_hero.jpg`: Dominant, polished golden retriever hero image on homepage.
  - `vet_holding_dog.jpg`: Prominent photograph in About Us and clinic introduction sections.
  - `vetnest_template.jpg`: Visual blueprint reference.
  - `images/clinic/`: Additional clinic and veterinary-team photographs.
  - `images/services/`: Service and gallery photography.

---

## 💻 Technology Stack

- **Backend Framework:** Django (Python 3.11 / 3.12 / 3.14)
- **Database:** SQLite (local development) / PostgreSQL (production on Render via `dj-database-url`)
- **Static Assets Serving:** WhiteNoise with compressed manifest storage
- **WSGI Production Server:** Gunicorn
- **Deployment Platform:** Render (Web Service via `render.yaml` and `build.sh`)

---

## 🚀 Pages & Features

### Public Portal
- **Homepage (`/`):** Hero section with dominant golden retriever portrait, 4 feature badges (*Experienced Veterinarians*, *Comprehensive Care Services*, *Modern Facilities*, *Personalized Treatment*), About clinic section with veterinarian holding dog photograph, database-driven services grid, 4-step booking workflow, and gallery preview.
- **About Us (`/about_us/`):** Clinic story, 3 stats counters (*10+ Years of Experience*, *2K+ Happy Pet Owners*, *5K+ Pets Treated*), veterinarian photograph, mission card with paw icon, and specialized care programs.
- **Services (`/services/`):** Full catalog of clinical treatments and procedures with booking buttons.
- **Category Details (`/category/<category_name>/`):** Specialized care modules (Wildlife, Emergency, Rehabilitation, Exotic Pets, Consulting, etc.) with checkmark benefit points and booking CTA.
- **Gallery (`/gallery/`):** "Cherished Moments" photo gallery with interactive category filters (*All*, *Dogs*, *Cats*, *Our Clinic*) and rounded image cards with hover captions.
- **Contact (`/contact/`):** 4 contact cards (Location, Phone, Email, Hours) with orange circular icons, Google Maps embed, and contact/feedback form.

### Pet Owner Portal
- **Authentication (`/login/`, `/register/`):** Role-based sign-in and registration with VETNEST styling.
- **User Dashboard (`/dashboard/`):** Real-time booking metrics (Total, Approved, Pending, Completed), profile summary banner, and recent visit log.
- **Book Appointment (`/create_appointment/`):** 4-step progress indicator (*1 Pet Details*, *2 Service*, *3 Date & Time*, *4 Confirmation*), server validation, past date blocking, and duplicate prevention.
- **My Appointments (`/appointments/`):** Filter tabs (*All*, *Confirmed*, *Pending*, *Cancelled*), pet avatar cards, and status badges.
- **Edit Profile (`/edit-profile/`):** User profile details and password updating.

### Administration Command Center
- **Admin Dashboard (`/admin-dashboard/`):** VETNEST themed dashboard with real-time KPI metric widgets, quick navigation toolbar, and client summary.
- **Pending Review (`/admin-pending/`):** Triage workflow to review and approve or reject incoming requests.
- **Active Appointments (`/admin-appointments/`):** Management of approved visits with direct *Mark Done* action.
- **Completed Archive (`/completed-appointments/`):** Historical archive of concluded pet visits.
- **Cancelled Archive (`/admin-cancelled/`):** Log of declined appointments.
- **Customer Messages (`/admin-feedback/`):** Clean feedback cards with reply and delete actions.
- **Service Management (`/add-service/`):** Form to publish new medical services with title, description, and photo upload.
- **User Management (`/admin-users/`, `/edit-user/<id>/`):** Directory of client accounts with editing and removal controls.

---

## 🛠️ Local Development Setup

### 1. Clone & Navigate
```bash
git clone <repository-url>
cd vetcare
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Windows
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

### 5. Run Migrations & Collect Static
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Run Test Suite
```bash
python manage.py test
```

### 7. Start Local Server
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🌐 Deploying to Render

This project is pre-configured with `render.yaml` and `build.sh` for one-click deployment on Render:

1. **Push to GitHub / GitLab:**
   Ensure your changes are committed and pushed to your remote repository.

2. **Create a New Web Service on Render:**
   - Go to [dashboard.render.com](https://dashboard.render.com/)
   - Click **New +** > **Web Service**
   - Connect your repository
   - Choose **Python** as runtime

3. **Render Build & Start Settings:**
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn vetcare.wsgi:application`

4. **Environment Variables on Render:**
   Configure the following in the Render Dashboard (**Environment** tab):
   | Key | Value | Description |
   |---|---|---|
   | `DEBUG` | `False` | Disables debug mode in production |
   | `SECRET_KEY` | *(Click Generate or paste random 50+ char string)* | Django cryptographic key |
   | `ALLOWED_HOSTS` | `.onrender.com` | Allowed domains |
   | `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Trusted origins for CSRF |
   | `DATABASE_URL` | *(Optional - Render PostgreSQL connection string)* | Uses PostgreSQL if set, SQLite fallback |
   | `PYTHON_VERSION` | `3.11.9` | Python runtime version |
   | `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | Optional email notification backend |

---

## 🔒 Git Safety & Commit Instructions

To review, commit, and push changes to your repository:

```bash
git status
git diff
git add .
git commit -m "Redesign website to VETNEST theme with warm beige palette and dominant hero dog image"
git push origin master
```
