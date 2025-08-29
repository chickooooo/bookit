from django.urls import path
from show import views


urlpatterns = [
    path(
        route="trending/",
        view=views.TrendingShowsView.as_view(),
        name="trending-shows",
    ),
]
