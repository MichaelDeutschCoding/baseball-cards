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
    path('offers/<int:offer_id>', views.offer_details, name='offer-details'),
    path('offers/<int:offer_id>/comments', views.add_comment, name='add-comment'),
    path('offers/', views.view_offers, name='active-offers'),
    path('old-offers/', views.old_offers, name='old-offers'),
    path('new-offer/', views.new_offer, name='new-offer'),
    path('buy/<int:offer_id>', views.buy, name='buy'),
    path('transactions/', views.transaction_history, name='transaction-history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)