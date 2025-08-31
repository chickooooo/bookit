from rest_framework import serializers
from show.models import ShowModel


class TrendingShowSerializer(serializers.ModelSerializer):
    # get value of performer key using a custom method
    performer = serializers.SerializerMethodField()

    class Meta:
        model = ShowModel
        fields = ["id", "name", "performer", "banner_url"]

    def get_performer(self, obj):
        # get only performer name
        # and not the performer object dict
        return obj.performer.name
