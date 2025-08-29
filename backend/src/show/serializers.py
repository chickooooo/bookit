from rest_framework import serializers
from show.models import ShowModel


class TrendingShowSerializer(serializers.ModelSerializer):
    performer = serializers.SerializerMethodField()

    class Meta:
        model = ShowModel
        fields = ["id", "name", "performer", "banner_url"]

    def get_performer(self, obj):
        return obj.performer.name
