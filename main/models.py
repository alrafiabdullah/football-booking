from django.db import models
from django.contrib.auth.models import User


class BooleanDefaultModel(models.Model):
    is_active = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=999)
    map_link = models.URLField(max_length=999)

    class Meta:
        verbose_name_plural = 'Places'

    def __str__(self):
        return self.name


class MatchDay(BooleanDefaultModel):
    name = models.CharField(max_length=255)
    happening_at = models.DateTimeField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    photos_link = models.URLField(max_length=999)
    total_cost = models.IntegerField(default=4000)
    total_players = models.ManyToManyField(User)

    class Meta:
        ordering = ['-happening_at']
        verbose_name_plural = 'Match Days'

    def __str__(self):
        return self.name


class Vote(BooleanDefaultModel):
    is_going = models.BooleanField(default=False)
    is_not_going = models.BooleanField(default=False)
    match_day = models.ForeignKey(MatchDay, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Votes'

    def __str__(self):
        return self.voted_by.username
