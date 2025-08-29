from django.db import models
from core.models import VenueModel, PerformerModel


class ShowModel(models.Model):
    class TagChoices(models.TextChoices):
        TRENDING = "TRENDING", "Trending"
        POPULAR = "POPULAR", "Popular"

    name = models.CharField(max_length=256)
    performer = models.ForeignKey(
        to=PerformerModel,
        on_delete=models.CASCADE,
        related_name="shows",
    )
    venue = models.ForeignKey(
        to=VenueModel,
        on_delete=models.CASCADE,
        related_name="shows",
    )
    start_time = models.DateTimeField()
    duration = models.DurationField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=0)
    banner_url = models.URLField(max_length=256, null=True)
    poster_url = models.URLField(max_length=256, null=True)
    tag = models.CharField(
        max_length=32,
        choices=TagChoices.choices,
        null=True,
    )
    description = models.TextField()

    @classmethod
    def get_trending_shows(cls):
        """Retrieve all shows tagged as 'TRENDING' and return them.
        Optimized to avoid N+1 query issue by prefetching
        related performer objects."""

        return cls.objects.filter(
            tag=cls.TagChoices.TRENDING,
        ).select_related("performer")
