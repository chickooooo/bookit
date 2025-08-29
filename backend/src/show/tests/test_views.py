from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from show.models import ShowModel
from core.models import CityModel, VenueModel, PerformerModel


class TestTrendingShowsView(APITestCase):
    """Test cases for TrendingShowsView"""

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
        ShowModel.objects.create(
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
            name="Trending Show 2",
            performer=self.performer,
            venue=self.venue,
            start_time=timezone.now(),
            duration=timedelta(hours=2),
            ticket_price=80,
            banner_url="https://example.com/banner2.jpg",
            poster_url="https://example.com/poster2.jpg",
            tag=ShowModel.TagChoices.TRENDING,
            description="A popular event",
        )

    def test_get_trending_shows(self):
        """Test trending-shows API returns trending shows list"""
        endpoint = reverse("trending-shows")
        response = self.client.get(endpoint)

        # verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "status": "SUCCESS",
            "data": [
                {
                    "id": 1,
                    "name": "Trending Show",
                    "performer": "John Doe",
                    "banner_url": "https://example.com/banner.jpg",
                },
                {
                    "id": 2,
                    "name": "Trending Show 2",
                    "performer": "John Doe",
                    "banner_url": "https://example.com/banner2.jpg",
                },
            ],
        }
        self.assertEqual(response.json(), expected)


class TestTrendingShowsViewEmpty(APITestCase):
    """Test cases for TrendingShowsView empty response"""

    def test_get_trending_shows_empty(self):
        """Test trending-shows API returns empty list"""

        endpoint = reverse("trending-shows")
        response = self.client.get(endpoint)

        # verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "status": "SUCCESS",
            "data": [],
        }
        self.assertEqual(response.json(), expected)
