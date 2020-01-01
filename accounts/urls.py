from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('profile/', views.profile, name='profile'),
]