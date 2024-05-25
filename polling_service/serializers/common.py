from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polling_service.models import Poll, Vote
from nested import MenuSerializer
from restaurant_service.models import Menu


class PollSerializer(serializers.ModelSerializer):
    votes_count = serializers.ReadOnlyField()
    menus_count = serializers.ReadOnlyField()

    class Meta:
        model = Poll
        fields = (
            "id",
            "created_at",
            "is_closed",
            "votes_count",
            "menus_count",
        )


class PollDetailSerializer(serializers.ModelSerializer):
    menus = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = (
            "id",
            "created_at",
            "is_closed",
            "menus",
        )

    @staticmethod
    def get_menus(obj):
        menus = obj.menus.all()
        return MenuSerializer(menus, many=True).data


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ("employee", "poll", "created_at")


class VoteCreateSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(date_added=date.today()).select_related(
            "restaurant"
        )
    )

    class Meta:
        model = Vote
        fields = ("menu", "employee")
        read_only_fields = ("employee",)

    def create(self, validated_data):
        user = self.context["request"].user
        today = date.today()

        if Vote.objects.filter(employee=user, created_at=today).exists():
            raise ValidationError("You can vote only once a day.")

        vote = Vote.objects.create(**validated_data)
        return vote
