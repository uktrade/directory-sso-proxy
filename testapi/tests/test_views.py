from django.core.urlresolvers import reverse
from rest_framework import status

from config.settings import TEST_API_AUTH_TOKEN


def test_get_user_by_email_with_signed_client_and_testing_api_disabled(
        settings, signed_client):
    settings.TEST_API_ENABLE = False
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    query = {"token": TEST_API_AUTH_TOKEN}
    response = signed_client.get(url, query)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_by_email_with_signed_client(signed_client):
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    query = {"token": TEST_API_AUTH_TOKEN}
    response = signed_client.get(url, query)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_by_email_with_signed_client_and_invalid_token(signed_client):
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    query = {"token": "this_is_an_invalid_token"}
    response = signed_client.get(url, query)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_signed_request_without_user_required_email(signed_client):
    url = reverse('user_by_email', kwargs={"email": ""})
    query = {"token": TEST_API_AUTH_TOKEN}
    response = signed_client.get(url, query)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_by_email_with_unsigned_client_and_testing_api_disabled(
        settings, client):
    settings.TEST_API_ENABLE = False
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    query = {"token": TEST_API_AUTH_TOKEN}
    response = client.get(url, query)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_by_email_with_unsigned_client(client):
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    query = {"token": TEST_API_AUTH_TOKEN}
    response = client.get(url, query)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_by_email_with_unsigned_client_and_invalid_auth_token(client):
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    query = {"token": "this_is_an_invalid_token"}
    response = client.get(url, query)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_by_email_with_unsigned_client_without_auth_token(client):
    url = reverse('user_by_email', kwargs={"email": "some@user.com"})
    response = client.get(url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
