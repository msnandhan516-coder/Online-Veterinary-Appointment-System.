from django.contrib import admin
from .models import UserRegister,Appointment,Contact,Service

admin.site.register(UserRegister)
admin.site.register(Appointment)
admin.site.register(Contact)
admin.site.register(Service)