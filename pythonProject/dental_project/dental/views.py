from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, Doctor, Clinic, Review


def index(request):
    services = Service.objects.filter(is_active=True)[:3]
    return render(request, 'index.html', {'services': services})


def about(request):
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, 'about.html', {'doctors': doctors})


@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return render(request, 'admin_panel.html', {'access_denied': True})

    services = Service.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'admin_panel.html', {
        'services': services,
        'doctors': doctors
    })


def catalog(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'catalog.html', {'services': services})


def contacts(request):
    clinics = Clinic.objects.all()
    return render(request, 'contacts.html', {'clinics': clinics})


@login_required
def entry(request):
    services = Service.objects.filter(is_active=True)
    doctors = Doctor.objects.filter(is_active=True)
    clinics = Clinic.objects.all()

    if request.method == 'POST':
        # Обработка формы записи
        pass

    return render(request, 'entry.html', {
        'services': services,
        'doctors': doctors,
        'clinics': clinics
    })


@login_required
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except:
        profile = None

    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_date')

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'appointments': appointments
    })