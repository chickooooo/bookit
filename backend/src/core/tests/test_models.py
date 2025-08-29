from django.test import TestCase
from core.models import CityModel, VenueModel, PerformerModel


class TestCityModel(TestCase):
    """Test cases for CityModel"""

    def setUp(self):
        self.city1 = CityModel.objects.create(
            name="New Delhi", image_url="https://example.com/new-delhi.jpg"
        )
        self.city2 = CityModel.objects.create(
            name="Mumbai", image_url="https://example.com/mumbai.jpg"
        )

    def test_fields(self):
        """Test that city fields are correctly saved"""
        self.assertEqual(self.city1.name, "New Delhi")
        self.assertEqual(
            self.city1.image_url,
            "https://example.com/new-delhi.jpg",
        )

        self.assertEqual(self.city2.name, "Mumbai")
        self.assertEqual(
            self.city2.image_url,
            "https://example.com/mumbai.jpg",
        )

    def test_str_method(self):
        """Test that __str__() returns the city name"""
        self.assertEqual(str(self.city1), "New Delhi")
        self.assertEqual(str(self.city2), "Mumbai")

    def test_get_all_cities(self):
        """Test that get_all_cities() returns all city instances"""
        cities = CityModel.get_all_cities()
        self.assertEqual(cities.count(), 2)
        self.assertIn(self.city1, cities)
        self.assertIn(self.city2, cities)


class TestVenueModel(TestCase):
    """Test cases for VenueModel"""

    def setUp(self):
        self.city = CityModel.objects.create(
            name="Bangalore", image_url="https://example.com/bangalore.jpg"
        )
        self.venue1 = VenueModel.objects.create(
            name="Stadium A",
            city=self.city,
        )
        self.venue2 = VenueModel.objects.create(
            name="Stadium B",
            city=self.city,
        )

    def test_fields(self):
        """Test that venue fields are correctly saved"""
        self.assertEqual(self.venue1.name, "Stadium A")
        self.assertEqual(self.venue1.city.name, "Bangalore")

        self.assertEqual(self.venue2.name, "Stadium B")
        self.assertEqual(self.venue2.city, self.city)

    def test_str_method(self):
        """Test that __str__() returns the venue name"""
        self.assertEqual(str(self.venue1), "Stadium A")
        self.assertEqual(str(self.venue2), "Stadium B")

    def test_city_relation(self):
        """Test that venue is correctly linked to a city"""
        self.assertEqual(self.venue1.city, self.city)
        self.assertEqual(self.venue2.city.name, "Bangalore")
        # test reverse lookup
        self.assertEqual(
            self.city.venues.count(),  # type: ignore
            2,
        )


class TestPerformerModel(TestCase):
    """Test cases for PerformerModel"""

    def setUp(self):
        self.performer = PerformerModel.objects.create(
            name="John Doe",
            bio="A talented musician from nowhere.",
            image_url="https://example.com/johndoe.jpg",
        )

    def test_fields(self):
        """Test performer fields are correctly saved"""
        self.assertEqual(
            self.performer.bio,
            "A talented musician from nowhere.",
        )
        self.assertEqual(
            self.performer.image_url,
            "https://example.com/johndoe.jpg",
        )

    def test_str_method(self):
        """Test that __str__() returns the performer name"""
        self.assertEqual(str(self.performer), "John Doe")
