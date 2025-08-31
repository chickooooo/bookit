from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from core.models import CityModel, VenueModel, PerformerModel
from show.models import ShowModel
from show.serializers import TrendingShowSerializer


class TestTrendingShowSerializer(TestCase):
    """Test cases for TrendingShowSerializer"""

    def setUp(self):
        self.city = CityModel.objects.create(
            name="Mumbai",
            image_url="https://example.com/mumbai.jpg",
        )
        self.venue = VenueModel.objects.create(
            name="Concert Hall",
            city=self.city,
        )
        self.performer = PerformerModel.objects.create(
            name="John Doe",
            bio="A talented musician from nowhere.",
            image_url="https://example.com/johndoe.jpg",
        )

        self.show = ShowModel.objects.create(
            name="Amazing Show",
            performer=self.performer,
            venue=self.venue,
            start_time=timezone.now(),
            duration=timedelta(hours=2),
            ticket_price=50,
            banner_url="https://example.com/banner.jpg",
            poster_url="https://example.com/poster.jpg",
            tag=ShowModel.TagChoices.TRENDING,
            description="An amazing musical experience.",
        )

    def test_serializer_output(self):
        """Test TrendingShowSerializer returns expected fields and values"""
        serializer = TrendingShowSerializer(instance=self.show)
        expected_output = {
            "id": self.show.id,  # type: ignore
            "name": "Amazing Show",
            "performer": "John Doe",
            "banner_url": "https://example.com/banner.jpg",
        }
        self.assertEqual(serializer.data, expected_output)
