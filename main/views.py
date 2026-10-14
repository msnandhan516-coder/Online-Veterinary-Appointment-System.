# =========================
# IMPORTS
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from datetime import datetime

from .models import UserRegister, Appointment,Contact,Service

from django.views.decorators.cache import never_cache
# =========================
# PUBLIC PAGES
# =========================
def index(request):
    services = Service.objects.all()[:6]
    return render(request, 'index.html', {'services': services})


# =========================
# USER REGISTRATION
# =========================
def register_view(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone = request.POST.get("phone")
        role = request.POST.get("role")   # ✅ ADD THIS

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address")
            return redirect("register")

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits")
            return redirect("register")

        if UserRegister.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # Save user with role
        UserRegister.objects.create(
            fullname=fullname,
            email=email,
            username=username,
            password=password,
            phone=phone,
            role=role
        )

        return render(request, "registration_success.html")

    return render(request, "register.html")

# =========================
# USER LOGIN
# =========================
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = UserRegister.objects.filter(
            username=username,
            password=password,
            role=role
        ).first()

        if user:
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["role"] = user.role

            if role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("dashboard")
        else:
            messages.error(request, "Invalid Username, Password or Role")

    return render(request, "login.html")

def services(request):
    services = Service.objects.all()
    return render(request, "services.html", {"services": services})

# =========================
# USER DASHBOARD
# =========================

@never_cache
def user_dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = get_object_or_404(UserRegister, id=request.session["user_id"])
    user_appointments = Appointment.objects.filter(user=user).order_by('-appointment_date', '-appointment_time')

    context = {
        "user": user,
        "recent_appointments": user_appointments[:5],
        "total_appointments": user_appointments.count(),
        "pending_count": user_appointments.filter(status='Pending').count(),
        "approved_count": user_appointments.filter(status='Approved', work_status='Not Done').count(),
        "completed_count": user_appointments.filter(work_status='Done').count(),
    }

    return render(request, "user_dashboard.html", context)

# =========================
# USER APPOINTMENTS
# =========================
@never_cache
def appointments(request):

    if "user_id" not in request.session:
        return redirect("login")

    user_id = request.session["user_id"]

    appointments = Appointment.objects.filter(user_id=user_id).order_by('-appointment_date', '-appointment_time')

    return render(request, 'appointments.html', {
        'appointments': appointments
    })

@never_cache
def create_appointment(request):

    if "user_id" not in request.session:
        return redirect("login")

    user = get_object_or_404(UserRegister, id=request.session["user_id"])

    if request.method == "POST":
        date_str = request.POST.get("appointment_date")
        time_str = request.POST.get("appointment_time")
        service_id = request.POST.get("service")
        pet_name = request.POST.get("pet_name", "").strip()
        pet_breed = request.POST.get("pet_breed", "").strip()
        description = request.POST.get("description", "").strip()

        if not service_id or not date_str or not time_str or not pet_name:
            messages.error(request, "Please fill in all required fields.")
            return redirect("create_appointment")

        service = get_object_or_404(Service, id=service_id)

        try:
            appt_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            appt_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect("create_appointment")

        from django.utils import timezone
        if appt_date < timezone.now().date():
            messages.error(request, "Appointment date cannot be in the past.")
            return redirect("create_appointment")

        # Check for exact duplicate slot for this user
        existing_appt = Appointment.objects.filter(
            user=user,
            appointment_date=appt_date,
            appointment_time=appt_time,
            service=service
        ).exists()
        if existing_appt:
            messages.error(request, "You already have an appointment scheduled for this exact date, time and service.")
            return redirect("create_appointment")

        Appointment.objects.create(
            user=user,
            pet_name=pet_name,
            pet_breed=pet_breed,
            service=service,
            appointment_date=appt_date,
            appointment_time=appt_time,
            description=description,
            status='Pending'
        )
        messages.success(request, f"Appointment for {pet_name} booked successfully! Our clinic team will review and confirm your visit.")
        return redirect("appointments")

    services = Service.objects.all()
    selected_service_id = request.GET.get('service_id')

    return render(request, "create_appointment.html", {
        "services": services,
        "user": user,
        "selected_service_id": selected_service_id
    })

@never_cache
def edit_profile(request):

    username = request.session.get("username")

    user = UserRegister.objects.get(username=username)

    if request.method == "POST":

        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.password = request.POST.get("password")

        user.save()

        return redirect("dashboard")

    return render(request, "edit_profile.html", {"user": user})

# =========================
# ADMIN APPOINTMENT ACTIONS
# =========================

def approve_appointment(request, appointment_id):

    if "role" not in request.session or request.session["role"] != "admin":
        return redirect("login")

    appointment = get_object_or_404(Appointment, id=appointment_id)

    appointment.status = 'Approved'
    appointment.save()

    # Send email safely
    try:
        send_mail(
            "Appointment Approved 🐾 - VetCare Clinic",
            f"Dear {appointment.user.fullname},\n\nYour appointment for {appointment.pet_name} on {appointment.appointment_date} at {appointment.appointment_time} has been approved.\n\nThank you,\nVetCare Animal Clinic",
            settings.DEFAULT_FROM_EMAIL,
            [appointment.user.email],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.success(request, f"Appointment for {appointment.pet_name} approved successfully ✅")

    return redirect('admin_pending')

def reject_appointment(request, appointment_id):

    if "role" not in request.session or request.session["role"] != "admin":
        return redirect("login")

    appointment = get_object_or_404(Appointment, id=appointment_id)

    appointment.status = 'Rejected'
    appointment.save()

    try:
        send_mail(
            "Appointment Update ❌ - VetCare Clinic",
            f"Dear {appointment.user.fullname},\n\nUnfortunately your appointment request for {appointment.pet_name} on {appointment.appointment_date} could not be accommodated at this time.\n\nPlease contact the clinic or schedule an alternative slot.\n\nVetCare Animal Clinic",
            settings.DEFAULT_FROM_EMAIL,
            [appointment.user.email],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.error(request, f"Appointment for {appointment.pet_name} rejected ❌")

    return redirect('admin_pending')

# =========================
# ADMIN DASHBOARD
# =========================
@never_cache
def admin_dashboard(request):


    if request.session.get("role") != "admin":
        return redirect("login")

    total_users = UserRegister.objects.exclude(role='admin').count()

    total_appointments = Appointment.objects.filter(status="Approved").count()
    pending_appointments = Appointment.objects.filter(status="Pending").count()
    cancelled_appointments = Appointment.objects.filter(status="Rejected").count()

    contacts = Contact.objects.all().order_by('-id')
    total_contacts = contacts.count()
    completed_appointments_count = Appointment.objects.filter(work_status='Done').count()
    remaining_approved = Appointment.objects.filter(
        status="Approved",
        work_status="Not Done"
    ).count()

    return render(request, "admin_dashboard.html", {
        "total_users": total_users,
        "total_appointments": remaining_approved,
        "pending_appointments": pending_appointments,
        "cancelled_appointments": cancelled_appointments,
        "total_contacts": total_contacts,
        "completed_appointments_count": completed_appointments_count,
    })
@never_cache
def edit_admin_profile(request):
    username = request.session.get("username")

    user = UserRegister.objects.get(username=username)

    if request.method == "POST":
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        password = request.POST.get("password")
        if password:
            user.password = password   # ⚠️ Not secure (see note below)

        user.save()
        return redirect('admin_dashboard')

    return render(request, 'edit-admin_profile.html', {
        'user': user   # ✅ THIS FIXES YOUR ISSUE
    })
@never_cache
def admin_users(request):
    users = UserRegister.objects.exclude(role='admin')
    return render(request, 'users_details.html', {'users': users})
@never_cache
def edit_user(request, id):
    user = UserRegister.objects.get(id=id)

    if request.method == "POST":
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        password = request.POST.get("password")
        if password:   # only update if entered
            user.password = password

        user.save()
        return redirect('admin_users')

    return render(request, 'edit_user.html', {'user': user})
@never_cache
def delete_user(request, id):
    user = UserRegister.objects.get(id=id)
    user.delete()
    return redirect('admin_users')

@never_cache
def admin_appointments(request):
    appointments = Appointment.objects.filter(
        status="Approved",
        work_status="Not Done"

    )

    return render(request, "admin_appointments.html", {
        "appointments": appointments
    })

def mark_done(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.work_status = "Done"
    appointment.save()
    return redirect('admin_appointments')

@never_cache
def completed_appointments(request):
    appointments = Appointment.objects.filter(work_status='Done')
    return render(request, 'completed_appointments.html', {'appointments': appointments})


def admin_pending(request):
    appointments = Appointment.objects.filter(status="Pending")
    return render(request, "admin_pending.html", {
        "appointments": appointments
    })


def admin_cancelled(request):
    appointments = Appointment.objects.filter(status="Rejected")
    return render(request, "admin_cancelled.html", {
        "appointments": appointments
    })


def add_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        Service.objects.create(
            name=name,
            description=description,
            image=image
        )
        return redirect('services')

    return render(request, "add_service.html")

def feedbacks(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, "admin_feedback.html", {"contacts": contacts})

def view_feedbacks(request, id):
    contact = Contact.objects.get(id=id)
    return render(request, "view_contact.html", {"contact": contact})

def reply_feedbacks(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        reply_message = request.POST.get("reply")

        # Save reply
        contact.reply = reply_message
        contact.save()

        # Send email safely
        try:
            send_mail(
                subject="Reply to your Feedback - VetCare Clinic",
                message=reply_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=True,
            )
            messages.success(request, f"Reply sent successfully to {contact.email}!")
        except Exception:
            messages.success(request, f"Reply recorded for {contact.email}.")

    return redirect("feedbacks")

def delete_feedbacks(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect("admin_dashboard")





def about_us(request):
    return render(request, 'about_us.html')



def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message")
        )

        messages.success(request, "Your feedback has been sent successfully!")
        return redirect('contact')   # Prevent form resubmit

    return render(request, "contact.html")




def category_detail(request, category_name):

    content_data = {
        "wildlife": {
            "title": "Wildlife Care",
            "description": "We provide compassionate and specialized care for injured and rescued wildlife animals. Our clinic works closely with local rescue teams and conservation groups to ensure proper medical treatment, rehabilitation, and safe return to their natural habitat whenever possible.",
        },
        "rehabilitation": {
            "title": "Rehabilitation Services",
            "description": "Our rehabilitation services focus on helping pets recover safely after surgery, injury, or illness. Through guided therapy, nutritional planning, and continuous monitoring, we support a smooth and healthy recovery process for your beloved companions",
        },
        "exotic-pets": {
            "title": "Exotic Pets",
            "description": "We offer expert medical care for exotic pets including birds, reptiles, rabbits, and other unique animals. Our team understands the special needs of exotic species and provides tailored treatments using modern diagnostic tools.",
        },
        "health-medicine": {
            "title": "Health & Medicine",
            "description": "From routine checkups to preventive vaccinations and advanced treatments, we provide complete healthcare solutions for pets of all ages. Our goal is to ensure long-term wellness and early detection of potential health concerns.",
        },
        "consulting": {
            "title": "Consulting",
            "description": "Our veterinary consultation services provide professional advice on pet health, nutrition, behavioral concerns, and preventive care. We guide pet owners with personalized recommendations to maintain their pets’ overall well-being.",
        },
        "our-staff": {
            "title": "Our Staff",
            "description": "Our dedicated team of experienced veterinarians, nurses, and support staff are passionate about animal care. With years of expertise and a compassionate approach, they ensure every pet receives the highest level of attention and treatment.",
        },
        "animals-pets": {
            "title": "Animals & Pets",
            "description": "We offer comprehensive services for domestic animals and pets of all breeds and sizes. Whether it’s routine care, grooming advice, or medical support, we are committed to keeping your pets happy and healthy.",
        },
        "emergency": {
            "title": "Emergency Care",
            "description": "24/7 emergency veterinary services.Our emergency care services are available to handle urgent and life-threatening situations. With prompt response and advanced medical facilities, we are prepared to provide immediate support when your pet needs it most.",
        },

    }

    category = content_data.get(category_name)

    if not category:
        return render(request, "404.html")

    return render(request, "category_detail.html", category)


def logout_user(request):

    request.session.flush()   # clears all session data

    return redirect('login')  # redirect to login page