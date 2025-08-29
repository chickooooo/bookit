from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

from show.models import ShowModel
from core.models import CityModel, VenueModel, PerformerModel
from show.domain.show_client import ShowClient


class TestShowClient(TestCase):
    """Test cases for ShowClient"""

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
            bio="Performer Bio",
            image_url="https://example.com/performer.jpg",
        )

        # Trending show
        self.trending_show = ShowModel.objects.create(
            name="Trending Show",
            performer=self.performer,
            venue=self.venue,
            start_time=timezone.now(),
            duration=timedelta(hours=2),
            ticket_price=100,
            banner_url="https://example.com/banner.jpg",
            poster_url="https://example.com/poster.jpg",
            tag=ShowModel.TagChoices.TRENDING,
            description="A trending event",
        )

        # Non-trending show
        ShowModel.objects.create(
            name="Popular Show",
            performer=self.performer,
            venue=self.venue,
            start_time=timezone.now(),
            duration=timedelta(hours=2),
            ticket_price=80,
            banner_url="https://example.com/banner2.jpg",
            poster_url="https://example.com/poster2.jpg",
            tag=ShowModel.TagChoices.POPULAR,
            description="A popular event",
        )

    def test_get_trending_shows_fields(self):
        """Test that get_trending_shows returns only required fields"""
        client = ShowClient()
        results = client.get_trending_shows()
        expected_keys = {"id", "name", "performer", "banner_url"}
        self.assertEqual(set(results[0].keys()), expected_keys)

    def test_get_trending_shows_returns_only_trending(self):
        """Test that get_trending_shows returns only shows tagged as TRENDING"""
        client = ShowClient()
        results = client.get_trending_shows()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Trending Show")
        self.assertEqual(results[0]["performer"], "John Doe")
        self.assertEqual(results[0]["banner_url"], "https://example.com/banner.jpg")

    def test_get_trending_shows_returns_empty_list(self):
        """Test that get_trending_shows returns empty list if no TRENDING shows"""
        self.trending_show.tag = ShowModel.TagChoices.POPULAR
        self.trending_show.save()

        client = ShowClient()
        results = client.get_trending_shows()

        self.assertEqual(results, [])
