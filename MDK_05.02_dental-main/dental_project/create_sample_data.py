# create_sample_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dental_project.settings')
django.setup()

from django.contrib.auth.models import User
from dental.models import Doctor, Clinic, Service

def create_sample_data():
    # Создаем пользователей для врачей
    user1, created = User.objects.get_or_create(
        username='dr_ivanov',
        defaults={
            'first_name': 'Алексей',
            'last_name': 'Иванов',
            'email': 'ivanov@rx-dental.ru'
        }
    )
    if created:
        user1.set_password('password123')
        user1.save()

    user2, created = User.objects.get_or_create(
        username='dr_petrov',
        defaults={
            'first_name': 'Дмитрий',
            'last_name': 'Петров',
            'email': 'petrov@rx-dental.ru'
        }
    )
    if created:
        user2.set_password('password123')
        user2.save()

    user3, created = User.objects.get_or_create(
        username='dr_sidorova',
        defaults={
            'first_name': 'Мария',
            'last_name': 'Сидорова',
            'email': 'sidorova@rx-dental.ru'
        }
    )
    if created:
        user3.set_password('password123')
        user3.save()

    user4, created = User.objects.get_or_create(
        username='dr_kuznetsov',
        defaults={
            'first_name': 'Сергей',
            'last_name': 'Кузнецов',
            'email': 'kuznetsov@rx-dental.ru'
        }
    )
    if created:
        user4.set_password('password123')
        user4.save()

    # Создаем врачей
    doctors_data = [
        {
            'user': user1,
            'specialization': 'therapist',
            'experience': 12,
            'education': 'Казанский государственный медицинский университет, стоматологический факультет',
            'description': 'Специалист по терапевтической стоматологии с 12-летним опытом работы. Эксперт в лечении кариеса и пульпита.',
            'is_active': True
        },
        {
            'user': user2,
            'specialization': 'surgeon',
            'experience': 15,
            'education': 'Московский государственный медико-стоматологический университет',
            'description': 'Хирург-имплантолог с 15-летним стажем. Проводит сложные операции по удалению зубов и имплантации.',
            'is_active': True
        },
        {
            'user': user3,
            'specialization': 'orthodontist',
            'experience': 10,
            'education': 'Санкт-Петербургский государственный медицинский университет',
            'description': 'Ортодонт, специалист по исправлению прикуса. Работает с брекет-системами и элайнерами.',
            'is_active': True
        },
        {
            'user': user4,
            'specialization': 'hygienist',
            'experience': 8,
            'education': 'Самарский государственный медицинский университет',
            'description': 'Стоматолог-гигиенист. Специализируется на профессиональной чистке и отбеливании зубов.',
            'is_active': True
        }
    ]

    for doctor_data in doctors_data:
        Doctor.objects.get_or_create(
            user=doctor_data['user'],
            defaults=doctor_data
        )

    # Создаем клиники
    clinics_data = [
        {
            'name': 'RX Стоматология - Центральный филиал',
            'address': 'г. Альметьевск, ул. Ленина, 123',
            'phone': '+7 (111) 123-45-67',
            'email': 'central@rx-dental.ru',
            'working_hours': 'Пн-Пт: 9:00-21:00, Сб-Вс: 10:00-18:00',
            'description': 'Основной филиал клиники RX с современным оборудованием и полным спектром услуг.'
        },
        {
            'name': 'RX Стоматология - Северный филиал',
            'address': 'г. Альметьевск, ул. Советская, 45',
            'phone': '+7 (111) 123-45-68',
            'email': 'north@rx-dental.ru',
            'working_hours': 'Пн-Пт: 8:00-20:00, Сб: 9:00-17:00, Вс: выходной',
            'description': 'Современный филиал в северной части города. Специализируется на детской стоматологии.'
        },
        {
            'name': 'RX Стоматология - Южный филиал',
            'address': 'г. Альметьевск, пр. Строителей, 78',
            'phone': '+7 (111) 123-45-69',
            'email': 'south@rx-dental.ru',
            'working_hours': 'Пн-Пт: 10:00-22:00, Сб-Вс: 10:00-16:00',
            'description': 'Филил премиум-класса с индивидуальными кабинетами и VIP-обслуживанием.'
        }
    ]

    for clinic_data in clinics_data:
        Clinic.objects.get_or_create(
            name=clinic_data['name'],
            defaults=clinic_data
        )

    # Создаем базовые услуги если их нет
    services_data = [
        {
            'name': 'Лечение кариеса',
            'description': 'Устранение кариозных поражений с установкой современной пломбы',
            'price': 1500,
            'category': 'therapy',
            'is_active': True
        },
        {
            'name': 'Лечение пульпита',
            'description': 'Лечение нерва зуба с последующим пломбированием каналов',
            'price': 3500,
            'category': 'therapy',
            'is_active': True
        },
        {
            'name': 'Удаление зуба (простое)',
            'description': 'Безболезненное удаление зуба под местной анестезией',
            'price': 2000,
            'category': 'surgical',
            'is_active': True
        },
        {
            'name': 'Имплантация зуба',
            'description': 'Установка импланта с последующим протезированием',
            'price': 25000,
            'category': 'surgical',
            'is_active': True
        }
    ]

    for service_data in services_data:
        Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )

    print("Данные успешно созданы!")
    print("Врачи:", Doctor.objects.count())
    print("Клиники:", Clinic.objects.count())
    print("Услуги:", Service.objects.count())

if __name__ == '__main__':
    create_sample_data()