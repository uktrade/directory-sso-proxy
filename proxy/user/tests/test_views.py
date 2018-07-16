from unittest.mock import patch

from django.core.urlresolvers import reverse
import pytest
import revproxy


def test_404(client):
    response = client.get('/asdf/')
    assert response.status_code == 404


@pytest.mark.parametrize(
    'get_kwargs,expected_x_forwarded_for',
    (
        (
            # If no X-Forwarded-For header, it is set to REMOTE_ADDR
            dict(
                REMOTE_ADDR='4.3.2.1'
            ),
            '4.3.2.1',
        ),
        (
            # If X-Forwarded-For header, REMOTE_ADDR is appended to it
            dict(
                REMOTE_ADDR='4.3.2.1',
                HTTP_X_FORWARDED_FOR='1.2.3.4',
            ),
            '1.2.3.4, 4.3.2.1',
        ),
    ),
)
def test_x_forwarded_for(client, get_kwargs, expected_x_forwarded_for):
    with patch('revproxy.views.HTTP_POOLS', wraps=revproxy.views.HTTP_POOLS) \
            as mock_pool_manager:
        client.get('/anything/', **get_kwargs)
    headers = mock_pool_manager.urlopen.call_args[1]['headers']
    assert headers['X-Forwarded-For'] == expected_x_forwarded_for


def test_if_x_forwarded_for_on_original_request_then_its_appended_to(client):
    with patch('revproxy.views.HTTP_POOLS', wraps=revproxy.views.HTTP_POOLS) \
            as mock_pool_manager:
        client.get('/anything/', REMOTE_ADDR='4.3.2.1',
                   HTTP_X_FORWARDED_FOR='1.2.3.4')
    headers = mock_pool_manager.urlopen.call_args[1]['headers']
    assert headers['X-Forwarded-For'] == '1.2.3.4, 4.3.2.1'


def test_account_signup(client):
    response = client.get(reverse('account_signup_proxy'))
    assert response.status_code == 200


def test_account_signup_next(client):
    response = client.get(reverse('account_signup_proxy') + (
        '?next=http%3A//www.example.com/test/next'
    ))
    assert response.status_code == 200


def test_account_login(client):
    response = client.get(reverse('account_login_proxy'))
    assert response.status_code == 200


def test_account_logout(client):
    response = client.get(reverse('account_logout_proxy'))
    assert response.status_code == 302


def test_inactive(client):
    response = client.get(reverse('account_inactive_proxy'))
    assert response.status_code == 200


def test_account_email_verification_sent(client):
    url = reverse('account_email_verification_sent_proxy')
    response = client.get(url)
    assert response.status_code == 200


def test_account_confirm_email(client):
    response = client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_account_confirm_email_next(client):
    response = client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ) + '?next=http%3A//www.example.com/test/next')

    assert response.status_code == 200


def test_account_set_password(client):
    response = client.get(reverse('account_set_password_proxy'))
    assert response.status_code == 302


def test_account_reset_password(client):
    response = client.get(reverse('account_reset_password_proxy'))
    assert response.status_code == 200


def test_account_reset_password_next(client):
    response = client.get(reverse('account_reset_password_proxy') + (
        '?next=http%3A//www.example.com/test/next'
    ))
    assert response.status_code == 200


def test_account_change_password(client):
    response = client.get(reverse('account_change_password_proxy'))
    assert response.status_code == 302


def test_account_reset_password_done(client):
    response = client.get(reverse('account_reset_password_done_proxy'))
    assert response.status_code == 200


def test_account_reset_password_from_key(client):
    response = client.get(reverse(
        'account_reset_password_from_key_proxy',
        kwargs={'uidb36': 'asdf', 'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_sso_root_proxy(client):
    response = client.get(reverse('sso_root_proxy'))
    assert response.status_code == 302
