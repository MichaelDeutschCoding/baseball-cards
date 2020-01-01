from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('error', views.error_page, name='error-page'),
    path('home/', views.index, name='home'),
    path('deck/', views.user_deck, name='view-deck'),
    path('deck/new', views.new_deck, name='new-deck'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)