from django.contrib import admin
from .models import Service, Doctor, Clinic, Appointment, Review, UserProfile


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'specialization', 'experience', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['user__first_name', 'user__last_name']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_full_name.short_description = 'Врач'


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name', 'address']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'service', 'doctor', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_date', 'clinic']
    search_fields = ['patient__username', 'service__name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['user__username', 'comment']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']
    search_fields = ['user__username', 'phone', 'city']