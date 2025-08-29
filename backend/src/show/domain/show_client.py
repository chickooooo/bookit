from typing import List, Dict
from show.models import ShowModel
from show.serializers import TrendingShowSerializer


class ShowClient:
    """Client class for Show app"""

    def get_trending_shows(self) -> List[Dict]:
        """
        Retrieve trending shows and returns as a list of dictionaries.

        Sample Response:
            {
                "id": 1,
                "name": "Amazing Show",
                "performer": "John Doe",
                "banner_url": "https://example.com/banner.jpg",
            }
        """
        trending_shows = ShowModel.get_trending_shows()
        serializer = TrendingShowSerializer(trending_shows, many=True)

        return serializer.data  # type: ignore
