from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestTrendingShowsView(APITestCase):
    """Test cases for TrendingShowsView"""

    @patch("show.views.ShowClient.get_trending_shows")
    def test_get_trending_shows(self, mock_get_trending_shows):
        """Test trending-shows API returns trending shows list"""

        # setup mock data
        show_data = [
            {
                "id": 1,
                "name": "Trending Show",
                "performer": "John Doe",
                "banner_url": "https://example.com/banner.jpg",
            }
        ]
        mock_get_trending_shows.return_value = show_data

        # make API request
        endpoint = reverse("trending-shows")
        response = self.client.get(endpoint)

        # verify that mock method was called once
        mock_get_trending_shows.assert_called_once()

        # verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "status": "SUCCESS",
            "data": show_data,
        }
        self.assertEqual(response.json(), expected)


class TestTrendingShowsViewEmpty(APITestCase):
    """Test cases for TrendingShowsView empty response"""

    @patch("show.views.ShowClient.get_trending_shows")
    def test_get_trending_shows_empty(self, mock_get_trending_shows):
        """Test trending-shows API returns empty list"""
        # setup mock data
        mock_get_trending_shows.return_value = []

        # make API request
        endpoint = reverse("trending-shows")
        response = self.client.get(endpoint)

        # verify that mock method was called once
        mock_get_trending_shows.assert_called_once()

        # verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "status": "SUCCESS",
            "data": [],
        }
        self.assertEqual(response.json(), expected)
