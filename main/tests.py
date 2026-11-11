from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date, time
from .models import UserRegister, Service, Appointment, Contact

class VetCareSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test service
        self.service = Service.objects.create(
            name="General Checkup",
            description="Complete clinical wellness checkup for pets."
        )
        # Create test regular user
        self.user = UserRegister.objects.create(
            fullname="Test Owner",
            email="owner@example.com",
            username="testowner",
            password="securepassword123",
            phone="9876543210",
            role="user"
        )
        # Create test admin user
        self.admin = UserRegister.objects.create(
            fullname="Clinic Admin",
            email="admin@example.com",
            username="testadmin",
            password="adminpassword123",
            phone="9876543211",
            role="admin"
        )

    def test_public_pages_render(self):
        """Verify all public facing pages render with 200 OK"""
        pages = [
            reverse('index'),
            reverse('about_us'),
            reverse('services'),
            reverse('gallery'),
            reverse('contact'),
            reverse('login'),
            reverse('register'),
            reverse('category_detail', kwargs={'category_name': 'emergency'}),
            reverse('category_detail', kwargs={'category_name': 'health-medicine'}),
        ]
        for url in pages:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Page {url} failed to load.")
            self.assertContains(response, "VETNEST")

    def test_category_404_handler(self):
        """Verify invalid category returns 404 or custom 404 template"""
        response = self.client.get(reverse('category_detail', kwargs={'category_name': 'nonexistent-category'}))
        self.assertEqual(response.status_code, 200) # Returns 404.html template
        self.assertContains(response, "Not Found")

    def test_contact_submission(self):
        """Verify contact feedback submission saves to database"""
        response = self.client.post(reverse('contact'), {
            'name': 'Visitor Jane',
            'email': 'jane@example.com',
            'phone': '1234567890',
            'message': 'Inquiring about pet vaccine packages.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email='jane@example.com').exists())

    def test_user_login_and_dashboard(self):
        """Verify user authentication session and dashboard access"""
        response = self.client.post(reverse('login'), {
            'username': 'testowner',
            'password': 'securepassword123',
            'role': 'user'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session.get('username'), 'testowner')
        self.assertEqual(self.client.session.get('role'), 'user')

        # Access user dashboard
        dash_response = self.client.get(reverse('dashboard'))
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, "Welcome, Test Owner")
        self.assertIn("no-store", dash_response["Cache-Control"])
        self.assertContains(dash_response, 'data-authenticated="true"')

        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)
        self.assertIn("no-store", logout_response["Cache-Control"])
        self.assertNotIn("user_id", self.client.session)

        dashboard_after_logout = self.client.get(reverse('dashboard'))
        self.assertRedirects(dashboard_after_logout, reverse('login'))

    def test_appointment_creation_and_past_date_validation(self):
        """Verify past dates are rejected and valid future appointments succeed"""
        # Log in as user
        session = self.client.session
        session['user_id'] = self.user.id
        session['username'] = self.user.username
        session['role'] = 'user'
        session.save()

        # Try booking in the past
        past_date = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
        response = self.client.post(reverse('create_appointment'), {
            'service': self.service.id,
            'pet_name': 'Milo',
            'pet_breed': 'Beagle',
            'appointment_date': past_date,
            'appointment_time': '10:00',
            'description': 'Checkup'
        }, follow=True)
        self.assertContains(response, "cannot be in the past")
        self.assertFalse(Appointment.objects.filter(pet_name='Milo').exists())

        # Book for tomorrow
        future_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        response_valid = self.client.post(reverse('create_appointment'), {
            'service': self.service.id,
            'pet_name': 'Milo',
            'pet_breed': 'Beagle',
            'appointment_date': future_date,
            'appointment_time': '10:00',
            'description': 'Annual Vaccination'
        }, follow=True)
        self.assertEqual(response_valid.status_code, 200)
        self.assertTrue(Appointment.objects.filter(pet_name='Milo').exists())
        appt = Appointment.objects.get(pet_name='Milo')
        self.assertEqual(appt.status, 'Pending')

    def test_admin_approval_and_completion_workflow(self):
        """Verify appointment approval, rejection, and completion by admin"""
        # Create an appointment
        future_date = date.today() + timedelta(days=3)
        appt = Appointment.objects.create(
            user=self.user,
            pet_name="Bella",
            pet_breed="Persian",
            service=self.service,
            appointment_date=future_date,
            appointment_time=time(14, 0),
            status="Pending"
        )

        # Log in as admin
        session = self.client.session
        session['user_id'] = self.admin.id
        session['username'] = self.admin.username
        session['role'] = 'admin'
        session.save()

        # Admin dashboard renders
        admin_dash = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(admin_dash.status_code, 200)

        # Approve appointment
        approve_resp = self.client.get(reverse('approve_appointment', kwargs={'appointment_id': appt.id}), follow=True)
        self.assertEqual(approve_resp.status_code, 200)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'Approved')

        # Mark done
        done_resp = self.client.get(reverse('mark_done', kwargs={'id': appt.id}), follow=True)
        self.assertEqual(done_resp.status_code, 200)

        logout_resp = self.client.get(reverse('logout'))
        self.assertEqual(logout_resp.status_code, 302)
        self.assertNotIn('user_id', self.client.session)
        self.assertNotIn('role', self.client.session)
        self.assertIn('no-store', logout_resp['Cache-Control'])

        admin_dash_after_logout = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(admin_dash_after_logout, reverse('login'))
        appt.refresh_from_db()
        self.assertEqual(appt.work_status, 'Done')
