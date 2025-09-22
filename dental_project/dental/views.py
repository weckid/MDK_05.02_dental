from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Service, Doctor, Clinic, Review, UserProfile, Appointment
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, AppointmentForm, ReviewForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('index')


def index(request):
    services = Service.objects.filter(is_active=True)[:3]
    reviews = Review.objects.filter(is_approved=True)[:5]
    return render(request, 'index.html', {
        'services': services,
        'reviews': reviews
    })


def about(request):
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, 'about.html', {'doctors': doctors})


@login_required
def admin_panel(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к админ панели.')
        return redirect('index')

    services = Service.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all().order_by('-created_at')[:10]

    return render(request, 'admin_panel.html', {
        'services': services,
        'doctors': doctors,
        'appointments': appointments
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
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Запись на прием создана успешно!')
            return redirect('profile')
    else:
        form = AppointmentForm()

    return render(request, 'entry.html', {
        'services': services,
        'doctors': doctors,
        'clinics': clinics,
        'form': form
    })


@login_required
def profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен успешно!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_date')

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'form': form,
        'appointments': appointments
    })


@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('index')
    return redirect('entry')