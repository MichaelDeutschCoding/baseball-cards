from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Team, Player


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    favorite_player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    about = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f" Profile: {self.user}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

