from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from show.domain.show_client import ShowClient


class TrendingShowsView(APIView):
    """View for trending shows"""

    def get(self, request: Request) -> Response:
        client = ShowClient()
        trending_shows = client.get_trending_shows()

        return Response(
            data={
                "status": "SUCCESS",
                "data": trending_shows,
            },
            status=status.HTTP_200_OK,
        )
