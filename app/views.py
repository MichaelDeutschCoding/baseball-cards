from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from random import choice
from .models import Deck, Card, Player
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def landing(request):
    return render(request, 'landing.html')

def error_page(request):
    return render(request, 'error.html')

@login_required
def user_deck(request):
    try:
        deck = request.user.profile.deck
    except Deck.DoesNotExist:
        return redirect(reverse('error-page'))

    return render(request, 'app/deck.html', {
        'deck': deck,
        'cards': deck.card_set.all()
    })


@login_required
def new_deck(request):
    profile = request.user.profile
    fav_team = profile.favorite_team

    if not (profile.favorite_player and profile.favorite_team):
        messages.error(request, "No cards added. Please choose a favorite team and player in your profile page first.")
        return redirect(reverse('error-page'))

    deck, created = Deck.objects.get_or_create(user_profile=profile)
    if not created:
        messages.warning(request, "Nice try, buddy. You've already got a deck!")
        return redirect(reverse('view-deck'))

    Card.objects.create(player=profile.favorite_player, owner=deck)

    for _ in range(3):
        random_player = choice(fav_team.player_set.all())
        Card.objects.create(player=random_player, owner=deck)

    for _ in range(15):
        random_player = choice(Player.objects.all())
        Card.objects.create(player=random_player, owner=deck)

    return redirect(reverse('view-deck'))

