from django.db import models


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
    scoring_code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    abbrev = models.CharField(max_length=2)

    def __str__(self):
        return self.abbrev

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=63)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} plays {self.position} for the {self.team}"
