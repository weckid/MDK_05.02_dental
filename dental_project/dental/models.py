from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('therapy', 'Терапевтическая стоматология'),
        ('surgical', 'Хирургическая стоматология'),
        ('medic', 'Лечение и реабилитация'),
        ('product', 'Товары'),
        ('diagnost', 'Диагностика'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    image = models.ImageField(upload_to='services/', verbose_name="Изображение", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('therapist', 'Терапевт'),
        ('surgeon', 'Хирург'),
        ('orthodontist', 'Ортодонт'),
        ('pediatric', 'Детский стоматолог'),
        ('hygienist', 'Гигиенист'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, verbose_name="Специализация")
    experience = models.IntegerField(verbose_name="Стаж работы (лет)")
    education = models.TextField(verbose_name="Образование")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='doctors/', verbose_name="Фото", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Clinic(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название клиники")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.TextField(verbose_name="Часы работы")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Клиника"
        verbose_name_plural = "Клиники"

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пациент")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name="Клиника")
    appointment_date = models.DateTimeField(verbose_name="Дата и время приема")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    notes = models.TextField(blank=True, verbose_name="Примечания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.patient.username} - {self.service.name} - {self.appointment_date}"


class Review(models.Model):
    RATING_CHOICES = [
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Удовлетворительно'),
        (2, 'Плохо'),
        (1, 'Ужасно'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.rating} звезд"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    address = models.TextField(verbose_name="Адрес", blank=True)
    city = models.CharField(max_length=100, verbose_name="Город", blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватар", null=True, blank=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    address = models.TextField(verbose_name="Адрес", blank=True)
    city = models.CharField(max_length=100, verbose_name="Город", blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватар", null=True, blank=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.user.username


# Сигнал для автоматического создания профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()