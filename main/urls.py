from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.user_dashboard, name="dashboard"),
    path('appointments/', views.appointments, name='appointments'),
    path('create-appointment/', views.create_appointment, name='create_appointment'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('edit_admin_profile/', views.edit_admin_profile, name='edit_admin_profile'),
    path('admin-appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin-pending/', views.admin_pending, name='admin_pending'),
    path("admin-feedback/", views.feedbacks, name="feedbacks"),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path("admin-cancelled/", views.admin_cancelled, name="admin_cancelled"),
    path("about_us/", views.about_us, name="about_us"),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path("contact/", views.contact, name="contact"),
    path("view-contact/<int:id>/", views.view_feedbacks, name="view_contact"),
    path("reply-contact/<int:id>/", views.reply_feedbacks, name="reply_contact"),
    path("delete-contact/<int:id>/", views.delete_feedbacks, name="delete_contact"),
    path("category/<str:category_name>/", views.category_detail, name="category_detail"),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('mark-done/<int:id>/', views.mark_done, name='mark_done'),
    path('completed-appointments/', views.completed_appointments, name='completed_appointments'),
    path('add-service/', views.add_service, name='add_service'),
    path('logout/', views.logout_user, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

