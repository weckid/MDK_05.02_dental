from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('catalog/', views.catalog, name='catalog'),
    path('contacts/', views.contacts, name='contacts'),
    path('entry/', views.entry, name='entry'),
    path('profile/', views.profile, name='profile'),

    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('appointment/create/', views.create_appointment, name='create_appointment'),
    path('review/create/', views.create_review, name='create_review'),
]