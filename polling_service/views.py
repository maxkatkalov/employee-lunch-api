import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.response import Response

from .models import Poll, Vote
from serializers.common import (
    PollSerializer,
    PollDetailSerializer,
    VoteSerializer,
    VoteCreateSerializer,
)
from .permissions import IsSuperuserOrEmployee


class DefaultSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 1000


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticated, IsSuperuserOrEmployee)
    pagination_class = DefaultSetPagination

    def get_queryset(self):
        if self.action == "list":
            queryset = self.queryset.annotate(
                votes_count=Count(
                    "votes", distinct=True, filter=~Q(votes__isnull=True)
                ),
                menus_count=Count(
                    "menus", distinct=True, filter=~Q(menus__isnull=True)
                ),
            )
            return queryset
        if self.action == "current_day":
            today = timezone.now().date()
            return self.queryset.get(created_at=today)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ("current_day", "retrieve"):
            return PollDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"], url_path="current-day")
    def current_day(self, request):
        today = datetime.date.today()

        try:
            poll = Poll.objects.get(created_at=today)
            serializer = PollDetailSerializer(poll)
            return Response(serializer.data)
        except Poll.DoesNotExist:
            return Response(
                {"error": "No poll available for today"}, status=404
            )


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated, IsSuperuserOrEmployee)
    pagination_class = DefaultSetPagination

    def get_serializer_class(self):
        if self.action in ("create", "partial_update", "update"):
            return VoteCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        return (
            self.queryset.filter(employee=self.request.user)
            .select_related("poll", "menu")
            .prefetch_related("menu__restaurant")
        )

    def perform_create(self, serializer):
        poll = Poll.objects.get(created_at=datetime.date.today())
        serializer.save(employee=self.request.user, poll=poll)
