from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class TrendingShowsView(APIView):
    """View for trending shows"""

    def get(self, request: Request) -> Response:
        return Response(
            data={"success": True},
            status=status.HTTP_200_OK,
        )
