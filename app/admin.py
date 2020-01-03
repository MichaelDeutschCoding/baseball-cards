from django.contrib import admin
from app.models import Deck, Player, Card, Offer, Comment, Transaction
# Register your models here.

admin.site.register(Deck)
admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Offer)
admin.site.register(Comment)
admin.site.register(Transaction)
