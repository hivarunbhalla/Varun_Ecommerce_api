from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

# BEST-PRACTICE: add those fixture here that will be used in all test modules

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff = False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate