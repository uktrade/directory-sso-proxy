from unittest.mock import patch

from django.urls import set_urlconf

from django.core.urlresolvers import reverse
from django.test.client import Client
import pytest
import revproxy


def test_404(client):
    response = client.get('/asdf/')
    assert response.status_code == 404


@pytest.fixture
def no_remote_addr_client():
    # The django test client _always_ populates REMOTE_ADDR
    # However, in production this depends on the web-server
    # environment, and we want to test the case when it's not
    # set.
    class NoRemoteAddrClient(Client):
        def _base_environ(self, **request):
            return {
                key: value
                for key, value in super()._base_environ(**request).items()
                if key != 'REMOTE_ADDR'
            }

    return NoRemoteAddrClient()


@pytest.mark.parametrize(
    'get_kwargs',
    (
        (
            # If neither X-Forwarded-For nor REMOTE_ADDR, then don't set
            # X-Forwarded-For outgoing
            dict(
            )
        ),
        (
            # If only REMOTE_ADDR, then don't set X-Forwarded-For outgoing
            dict(
                REMOTE_ADDR='4.3.2.1'
            )
        ),
        (
            # If only X-Forwarded-For incomding, then don't set
            # X-Forwarded-For outgoing
            dict(
                HTTP_X_FORWARDED_FOR='1.2.3.4',
            )
        ),
    ),
)
def test_x_forwarded_for_not_set(no_remote_addr_client, get_kwargs, settings):
    settings.FEATURE_URL_PREFIX_ENABLED = True
    set_urlconf('conf.urls')

    stub = patch('revproxy.views.HTTP_POOLS', wraps=revproxy.views.HTTP_POOLS)
    with stub as mock_pool_manager:
        no_remote_addr_client.get('/sso/accounts/login/', **get_kwargs)
    headers = mock_pool_manager.urlopen.call_args[1]['headers']
    assert 'X-Forwarded-For' not in headers


def test_if_x_forwarded_for_and_remote_addr_then_are_concat_with_comma(
    client, settings
):
    settings.FEATURE_URL_PREFIX_ENABLED = True
    set_urlconf('conf.urls')

    stub = patch('revproxy.views.HTTP_POOLS', wraps=revproxy.views.HTTP_POOLS)
    with stub as mock_pool_manager:
        client.get(
            '/sso/accounts/login/',
            REMOTE_ADDR='4.3.2.1',
            HTTP_X_FORWARDED_FOR='1.2.3.4',
        )
    headers = mock_pool_manager.urlopen.call_args[1]['headers']
    assert headers['X-Forwarded-For'] == '1.2.3.4, 4.3.2.1'


def test_account_signup(authenticated_client):
    response = authenticated_client.get(reverse('account_signup_proxy'))
    assert response.status_code == 200


def test_account_signup_next(authenticated_client):
    response = authenticated_client.get(reverse('account_signup_proxy') + (
        '?next=http%3A//www.example.com/test/next'
    ))
    assert response.status_code == 200


def test_account_login(authenticated_client):
    response = authenticated_client.get(reverse('account_login_proxy'))
    assert response.status_code == 200


def test_account_logout(authenticated_client):
    response = authenticated_client.get(reverse('account_logout_proxy'))
    assert response.status_code == 302


def test_inactive(authenticated_client):
    response = authenticated_client.get(reverse('account_inactive_proxy'))
    assert response.status_code == 200


def test_account_email_verification_sent(authenticated_client):
    url = reverse('account_email_verification_sent_proxy')
    response = authenticated_client.get(url)
    assert response.status_code == 200


def test_account_confirm_email(authenticated_client):
    response = authenticated_client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_account_confirm_email_next(authenticated_client):
    response = authenticated_client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ) + '?next=http%3A//www.example.com/test/next')

    assert response.status_code == 200


def test_account_set_password(authenticated_client):
    response = authenticated_client.get(reverse('account_set_password_proxy'))
    assert response.status_code == 302


def test_account_reset_password(authenticated_client):
    url = reverse('account_reset_password_proxy')
    response = authenticated_client.get(url)
    assert response.status_code == 200


def test_account_reset_password_next(authenticated_client):
    url = reverse('account_reset_password_proxy') + (
        '?next=http%3A//www.example.com/test/next'
    )
    response = authenticated_client.get(url)
    assert response.status_code == 200


def test_account_change_password(authenticated_client):
    url = reverse('account_change_password_proxy')
    response = authenticated_client.get(url)
    assert response.status_code == 302


def test_account_reset_password_done(authenticated_client):
    url = reverse('account_reset_password_done_proxy')
    response = authenticated_client.get(url)
    assert response.status_code == 200


def test_account_reset_password_from_key(authenticated_client):
    response = authenticated_client.get(reverse(
        'account_reset_password_from_key_proxy',
        kwargs={'uidb36': 'asdf', 'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_sso_root_proxy(authenticated_client):
    response = authenticated_client.get(reverse('sso_root_proxy'))
    assert response.status_code == 302
