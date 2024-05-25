from rest_framework.routers import DefaultRouter

from .views import PollViewSet, VoteViewSet

router = DefaultRouter()
router.register("polls", PollViewSet, basename="polls")
router.register("votes", VoteViewSet, basename="votes")

urlpatterns = router.urls

app_name = "polling"
