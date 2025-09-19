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
]