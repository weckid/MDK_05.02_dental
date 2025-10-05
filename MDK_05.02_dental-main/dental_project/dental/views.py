from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Service, Doctor, Clinic, Review, UserProfile, Appointment
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, AppointmentForm, ReviewForm
from datetime import datetime
import json


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
    doctors = Doctor.objects.filter(is_active=True)
    clinics = Clinic.objects.all()

    return render(request, 'catalog.html', {
        'services': services,
        'doctors': doctors,
        'clinics': clinics,
        'today': timezone.now().date()
    })


@require_POST
@csrf_exempt
def create_appointment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})

    try:
        service_id = request.POST.get('service_id')
        doctor_id = request.POST.get('doctor')
        clinic_id = request.POST.get('clinic')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        notes = request.POST.get('notes', '')

        # Валидация обязательных полей
        if not all([service_id, doctor_id, clinic_id, appointment_date, appointment_time]):
            return JsonResponse({'success': False, 'error': 'Все поля обязательны для заполнения'})

        # Создаем объект datetime из даты и времени
        appointment_datetime_naive = datetime.strptime(
            f"{appointment_date} {appointment_time}",
            "%Y-%m-%d %H:%M"
        )

        # Преобразуем в осведомленный datetime с временной зоной
        appointment_datetime = timezone.make_aware(appointment_datetime_naive)

        # Проверяем, что дата не в прошлом
        if appointment_datetime < timezone.now():
            return JsonResponse({'success': False, 'error': 'Нельзя записаться на прошедшую дату'})

        # Получаем объекты из базы данных
        service = Service.objects.get(id=service_id)
        doctor = Doctor.objects.get(id=doctor_id)
        clinic = Clinic.objects.get(id=clinic_id)

        # Проверяем, активен ли врач и услуга
        if not service.is_active:
            return JsonResponse({'success': False, 'error': 'Услуга неактивна'})
        if not doctor.is_active:
            return JsonResponse({'success': False, 'error': 'Врач неактивен'})

        # Создаем запись в базе данных
        appointment = Appointment.objects.create(
            patient=request.user,
            service=service,
            doctor=doctor,
            clinic=clinic,
            appointment_date=appointment_datetime,
            notes=notes,
            status='pending'
        )

        messages.success(request, 'Запись на прием успешно создана!')
        return JsonResponse({'success': True, 'appointment_id': appointment.id})

    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Услуга не найдена'})
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Врач не найден'})
    except Clinic.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Клиника не найдена'})
    except ValueError as e:
        return JsonResponse({'success': False, 'error': 'Неверный формат даты или времени'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Произошла ошибка: {str(e)}'})


@login_required
def update_appointment_status(request, appointment_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    if request.method == 'POST':
        try:
            new_status = request.POST.get('status')
            appointment = get_object_or_404(Appointment, id=appointment_id)

            # Валидация статуса
            valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
            if new_status not in valid_statuses:
                return JsonResponse({'success': False, 'error': 'Неверный статус'})

            appointment.status = new_status
            appointment.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Метод не разрешен'})


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

            # Преобразуем наивную дату в осведомленную
            if appointment.appointment_date and timezone.is_naive(appointment.appointment_date):
                appointment.appointment_date = timezone.make_aware(appointment.appointment_date)

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
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        # Обновляем данные пользователя
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # Обновляем профиль
        profile.phone = request.POST.get('phone', '')
        profile.birth_date = request.POST.get('birth_date') or None
        profile.city = request.POST.get('city', '')
        profile.address = request.POST.get('address', '')

        # Обработка аватара
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.save()

        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    # Получаем реальные записи пользователя из базы данных
    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_date')

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
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


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})