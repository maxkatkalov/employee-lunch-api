import pytest

from .factory_instances import UserFactory, RestaurantFactory, MenuFactory

pytestmark = pytest.mark.django_db


class TestRestaurantManagementViews:
    RESTAURANTS_URL = "/api/restaurants-management/restaurants/"
    MENUS_URL = "/api/restaurants-management/menus/"

    @pytest.mark.parametrize(
        "user, is_owner, is_superuser, status_code,",
        [
            (
                False,
                False,
                False,
                401,
            ),
            (
                True,
                False,
                False,
                200,
            ),
            (
                True,
                True,
                False,
                200,
            ),
            (
                True,
                False,
                True,
                200,
            )
        ]
    )
    def test_different_user_get_access_to_restaurants_list(
            self,
            api_client,
            user: bool,
            is_owner: bool,
            is_superuser: bool,
            status_code: int,
            endpoint_url: str = RESTAURANTS_URL,
    ):
        if user:
            user = UserFactory(is_owner=is_owner, is_superuser=is_superuser)
            restaurant = RestaurantFactory()
            if is_owner:
                restaurant.owner = user
                restaurant.save()

            api_client.force_authenticate(user=user)
            response = api_client.get(endpoint_url)
            response_detail = api_client.get(f"{endpoint_url}{restaurant.id}/")

            assert response.status_code == status_code
            assert response_detail.status_code == status_code
            assert response.json().get("count") == 1

        else:
            response_list = api_client.get(endpoint_url)

            assert response_list.status_code == 401
            assert response_list.json().get("detail") == "Authentication credentials were not provided."

    @pytest.mark.parametrize(
        "user, is_owner, is_superuser, status_code,",
        [
            (
                False,
                False,
                False,
                401,
            ),
            (
                True,
                False,
                False,
                403,
            ),
            (
                True,
                True,
                False,
                200,
            ),
            (
                True,
                False,
                True,
                200,
            )
        ]
    )
    def test_different_user_get_access_to_restaurants_detail(
            self,
            api_client,
            user: bool,
            is_owner: bool,
            is_superuser: bool,
            status_code: int,
            endpoint_url: str = MENUS_URL,
    ):
        if user:
            user = UserFactory(is_owner=is_owner, is_superuser=is_superuser)
            restaurant = RestaurantFactory()
            menu = MenuFactory(restaurant=restaurant)
            if is_owner:
                restaurant.owner = user
                restaurant.save()

            api_client.force_authenticate(user=user)
            response = api_client.get(endpoint_url)
            response_detail = api_client.get(f"{endpoint_url}{menu.id}/")

            assert response.status_code == status_code
            assert response_detail.status_code == status_code

            if user.is_owner:
                assert response.json().get("count") == 1

        else:
            response_list = api_client.get(endpoint_url)

            assert response_list.status_code == 401
            assert response_list.json().get("detail") == "Authentication credentials were not provided."

