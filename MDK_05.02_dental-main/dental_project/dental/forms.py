from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Appointment, Review


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя или Email")

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'birth_date', 'address', 'city', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'clinic', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительная информация'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
            'rating': forms.Select(
                choices=[(5, 'Отлично'), (4, 'Хорошо'), (3, 'Удовлетворительно'), (2, 'Плохо'), (1, 'Ужасно')]),
        }

        class CustomUserCreationForm(UserCreationForm):
            email = forms.EmailField(required=True, label="Email")
            first_name = forms.CharField(required=True, label="Имя")
            last_name = forms.CharField(required=True, label="Фамилия")

            class Meta:
                model = User
                fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        class CustomAuthenticationForm(AuthenticationForm):
            username = forms.CharField(label="Имя пользователя или Email")

            class Meta:
                model = User
                fields = ['username', 'password']

        class UserProfileForm(forms.ModelForm):
            class Meta:
                model = UserProfile
                fields = ['phone', 'birth_date', 'address', 'city', 'avatar']
                widgets = {
                    'birth_date': forms.DateInput(attrs={'type': 'date'}),
                    'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
                }

        class AppointmentForm(forms.ModelForm):
            class Meta:
                model = Appointment
                fields = ['service', 'doctor', 'clinic', 'appointment_date', 'notes']
                widgets = {
                    'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                    'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительная информация'}),
                }

        class ReviewForm(forms.ModelForm):
            class Meta:
                model = Review
                fields = ['rating', 'comment']
                widgets = {
                    'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
                    'rating': forms.Select(
                        choices=[(5, 'Отлично'), (4, 'Хорошо'), (3, 'Удовлетворительно'), (2, 'Плохо'), (1, 'Ужасно')]),
                }