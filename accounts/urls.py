from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('meeting/', views.meeting_manager, name='meeting'),
    path('save_meeting/', views.save_meeting, name='save_meeting'),
    path('profile_manager/', views.profile_manager, name='profile_manager'),
    path('edit_profile/', views.edit_profile, name = 'save_profile'),
    path('edit_delete/',views.edit_delete, name='edit_profile'),
    path('verification/', views.verify, name='verification'),
    path('checkout/', views.checkout, name='checkout')
]