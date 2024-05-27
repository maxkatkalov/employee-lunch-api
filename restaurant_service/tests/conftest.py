import pytest
from rest_framework.test import APIClient

from .factory_instances import UserFactory


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture
def authenticated_api_client(unauthenticated_api_client):
    user = UserFactory()
    unauthenticated_api_client.force_authenticate(user=user)
    yield unauthenticated_api_client
