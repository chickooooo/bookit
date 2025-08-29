from django.db import models
from core.models import VenueModel, PerformerModel


class ShowModel(models.Model):
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
    description = models.TextField()
