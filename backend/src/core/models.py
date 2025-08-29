from __future__ import annotations

from django.db import models
from django.db.models.manager import BaseManager


class CityModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image_url = models.URLField(max_length=256)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_cities(cls) -> BaseManager[CityModel]:
        return cls.objects.all()  # type: ignore


class VenueModel(models.Model):
    name = models.CharField(max_length=128)
    city = models.ForeignKey(
        CityModel,
        on_delete=models.CASCADE,
        related_name="venues",
    )

    def __str__(self):
        return self.name


class PerformerModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    bio = models.TextField()
    image_url = models.URLField(max_length=256)

    def __str__(self):
        return self.name
