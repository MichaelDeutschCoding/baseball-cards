import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from random import choice
from .forms import AddCommentForm
from .models import Deck, Card, Player, Offer, Comment

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

    all_cards = deck.card_set.all()
    paginator = Paginator(all_cards, 12)
    page = request.GET.get('page')
    cards = paginator.get_page(page)

    return render(request, 'app/deck.html', {
        'deck': deck,
        'paginator': paginator,
        'page_obj': cards
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

@login_required
def view_offers(request):
    offers = Offer.objects.filter(active=True)

    return render(request, 'app/offers.html', {'offers': offers})

@login_required
def offer_details(request, offer_id):
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        return redirect(reverse('error-page'))

    form = AddCommentForm()

    return render(request, 'app/offer.html', {
        'offer': offer,
        'card': offer.card,
        'comments': offer.comment_set.all(),
        'form': form,
    })

@login_required
def add_comment(request, offer_id):
    comment = json.loads(request.body)
    form = AddCommentForm(comment)
    comment = form.save(commit=False)
    comment.author = request.user.profile.deck
    comment.offer_id = offer_id
    comment.save()

    return JsonResponse({
        'comment_id': comment.pk
    }, status=201)