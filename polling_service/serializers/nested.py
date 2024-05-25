from rest_framework import serializers

from restaurant_service.models import Menu


class MenuSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = (
            "id",
            "name",
            "votes_count",
        )

    @staticmethod
    def get_votes_count(obj):
        return obj.votes.count()
