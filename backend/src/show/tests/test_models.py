from zoneinfo import ZoneInfo

from django.test import TestCase
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from show.models import ShowModel
from core.models import PerformerModel, VenueModel, CityModel


class TestShowModel(TestCase):
    """Test cases for ShowModel"""

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
            name="The Rockers",
            image_url="https://example.com/rockers.jpg",
        )
        self.show = ShowModel.objects.create(
            name="Rock Night",
            performer=self.performer,
            venue=self.venue,
            start_time=make_aware(
                datetime(2025, 9, 1, 20, 0),
                ZoneInfo("Asia/Kolkata"),
            ),
            duration=timedelta(hours=2),
            ticket_price=1500,
            banner_url="https://example.com/banner.jpg",
            poster_url="https://example.com/poster.jpg",
            description="An electrifying night of rock music!",
        )

    def test_fields(self):
        """Test that show fields are correctly saved"""
        self.assertEqual(self.show.name, "Rock Night")
        self.assertEqual(self.show.performer.name, "The Rockers")
        self.assertEqual(self.show.venue.name, "Concert Hall")
        self.assertEqual(
            self.show.start_time,
            make_aware(datetime(2025, 9, 1, 20, 0), ZoneInfo("Asia/Kolkata")),
        )
        self.assertEqual(self.show.duration, timedelta(hours=2))
        self.assertEqual(self.show.ticket_price, 1500)
        self.assertEqual(self.show.banner_url, "https://example.com/banner.jpg")
        self.assertEqual(self.show.poster_url, "https://example.com/poster.jpg")
        self.assertEqual(self.show.tag, None)
        self.assertEqual(self.show.description, "An electrifying night of rock music!")

    def test_performer_relation(self):
        """Test that show is correctly linked to a performer"""
        self.assertEqual(self.show.performer, self.performer)
        self.assertEqual(self.performer.shows.count(), 1)  # type: ignore
        self.assertIn(self.show, self.performer.shows.all())  # type: ignore

    def test_venue_relation(self):
        """Test that show is correctly linked to a venue"""
        self.assertEqual(self.show.venue, self.venue)
        self.assertEqual(self.venue.shows.count(), 1)  # type: ignore
        self.assertIn(self.show, self.venue.shows.all())  # type: ignore

    def test_get_trending_shows_returns_only_trending(self):
        """Test that get_trending_shows returns only shows with TRENDING tag"""
        trending_show = ShowModel.objects.create(
            name="Trending Show",
            performer=self.performer,
            venue=self.venue,
            start_time=make_aware(
                datetime(2025, 9, 2, 20, 0), ZoneInfo("Asia/Kolkata")
            ),
            duration=timedelta(hours=1),
            ticket_price=1000,
            banner_url="https://example.com/trending_banner.jpg",
            poster_url="https://example.com/trending_poster.jpg",
            tag=ShowModel.TagChoices.TRENDING,
            description="A trending performance!",
        )

        popular_show = ShowModel.objects.create(
            name="Popular Show",
            performer=self.performer,
            venue=self.venue,
            start_time=make_aware(
                datetime(2025, 9, 3, 20, 0), ZoneInfo("Asia/Kolkata")
            ),
            duration=timedelta(hours=1),
            ticket_price=1200,
            banner_url="https://example.com/popular_banner.jpg",
            poster_url="https://example.com/popular_poster.jpg",
            tag=ShowModel.TagChoices.POPULAR,
            description="A popular performance!",
        )

        trending_shows = ShowModel.get_trending_shows()

        self.assertEqual(trending_shows.count(), 1)
        self.assertIn(trending_show, trending_shows)
        self.assertNotIn(popular_show, trending_shows)

    def test_get_trending_shows_empty_when_no_trending(self):
        """Test that get_trending_shows returns empty queryset when no shows are trending"""
        self.show.tag = ShowModel.TagChoices.POPULAR
        self.show.save()

        trending_shows = ShowModel.get_trending_shows()
        self.assertEqual(trending_shows.count(), 0)

    def test_get_trending_shows_query_count(self):
        """Test that get_trending_shows executes only one query with select_related"""
        ShowModel.objects.create(
            name="Trending Show",
            performer=self.performer,
            venue=self.venue,
            start_time=make_aware(
                datetime(2025, 9, 2, 20, 0),
                ZoneInfo("Asia/Kolkata"),
            ),
            duration=timedelta(hours=1),
            ticket_price=1000,
            banner_url="https://example.com/trending_banner.jpg",
            poster_url="https://example.com/trending_poster.jpg",
            tag=ShowModel.TagChoices.TRENDING,
            description="A trending performance!",
        )

        with self.assertNumQueries(1):
            shows = list(ShowModel.get_trending_shows())
            for show in shows:
                show.performer.name  # uses select_related, no extra query
