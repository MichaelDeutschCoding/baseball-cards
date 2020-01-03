from random import random
from django.db import models


class NotEnoughCredits(Exception):
    pass

class TransactionWithSelf(Exception):
    pass

class AlreadySold(Exception):
    pass

class Deck(models.Model):
    user_profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE, primary_key=True)
    credits = models.IntegerField(default=500)

    def __str__(self):
        return f"{self.user_profile.user.username}"


class Team(models.Model):
    team_symbol = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=31)
    city = models.CharField(max_length=31)
    state = models.CharField(max_length=2)
    stadium = models.CharField(max_length=31)
    league = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=20)
    abbrev = models.CharField(max_length=2, primary_key=True)
    scoring_code = models.PositiveIntegerField()

    def __str__(self):
        return self.abbrev


class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=63)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/player_pics', default='media/player_pics/dimaggio.jpg')

    def __str__(self):
        return f"{self.position} - {self.name}  ({self.team})"


class HitterStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    avg = models.DecimalField(max_digits=5, decimal_places=3)
    slg = models.DecimalField(max_digits=5, decimal_places=3)
    ops = models.DecimalField(max_digits=5, decimal_places=3)
    hits = models.IntegerField()
    hr = models.IntegerField()
    rbi = models.IntegerField()
    so = models.IntegerField()


class PitcherStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    throws = models.CharField(max_length=1)
    k_per_9 = models.DecimalField(max_digits=5, decimal_places=2)
    bb_per_9 = models.DecimalField(max_digits=5, decimal_places=2)
    k_bb = models.DecimalField(max_digits=5, decimal_places=2)
    era = models.DecimalField(max_digits=5, decimal_places=2)
    innings = models.DecimalField(max_digits=5, decimal_places=1)


def is_signed():
    return random() > .8

class Card(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    owner = models.ForeignKey(Deck, on_delete=models.CASCADE)
    signed = models.BooleanField(default=is_signed)

    def __str__(self):
        return f"{self.player.position} - {self.player.name}  |   Signed: {self.signed} | Owner: {self.owner.user_profile.user} "

    def trade(self, new_owner):
        self.owner = new_owner
        self.save()

class Offer(models.Model):
    seller = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        status = f'available for {self.price} credits' if self.active else 'sold'
        return f"Card: {self.card.player} {status}"


class Comment(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    author = models.ForeignKey(Deck, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Deck, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"sold {self.offer.card.player} card on {self.date}"

    def save(self):
        if not self.offer.active:
            raise AlreadySold("Too late! Offer was already accepted.")

        if self.buyer.credits < self.offer.price:
            raise NotEnoughCredits("You do not have enough credits for this trade.")

        if self.buyer == self.offer.seller:
            raise TransactionWithSelf("You can't make a trade with yourself!")

        self.offer.card.trade(self.buyer)
        self.buyer.credits -= self.offer.price
        self.offer.seller.credits += self.offer.price
        self.buyer.save()
        self.offer.seller.save()

        Offer.objects.filter(card=self.offer.card).update(active=False)

        super().save()