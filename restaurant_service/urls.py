from rest_framework.routers import DefaultRouter

from .views import RestaurantViewSet, MenuViewSet

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurants")
router.register("menus", MenuViewSet, basename="menus")

urlpatterns = router.urls

app_name = "restaurant"
