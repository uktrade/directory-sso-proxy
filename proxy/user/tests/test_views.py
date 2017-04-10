from django.core.urlresolvers import reverse


def test_404(signed_client):
    response = signed_client.get('/asdf/')
    assert response.status_code == 404


def test_account_signup(signed_client):
    response = signed_client.get(reverse('account_signup_proxy'))
    assert response.status_code == 200


def test_account_signup_next(signed_client):
    response = signed_client.get(reverse('account_signup_proxy') + (
        '?next=http%3A//www.example.com/test/next'
    ))
    assert response.status_code == 200


def test_account_login(signed_client):
    response = signed_client.get(reverse('account_login_proxy'))
    assert response.status_code == 200


def test_account_logout(signed_client):
    response = signed_client.get(reverse('account_logout_proxy'))
    assert response.status_code == 302


def test_inactive(signed_client):
    response = signed_client.get(reverse('account_inactive_proxy'))
    assert response.status_code == 200


def test_account_email_verification_sent(signed_client):
    url = reverse('account_email_verification_sent_proxy')
    response = signed_client.get(url)
    assert response.status_code == 200


def test_account_confirm_email(signed_client):
    response = signed_client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_account_confirm_email_next(signed_client):
    response = signed_client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ) + '?next=http%3A//www.example.com/test/next')

    assert response.status_code == 200


def test_account_set_password(signed_client):
    response = signed_client.get(reverse('account_set_password_proxy'))
    assert response.status_code == 302


def test_account_reset_password(signed_client):
    response = signed_client.get(reverse('account_reset_password_proxy'))
    assert response.status_code == 200


def test_account_reset_password_next(signed_client):
    response = signed_client.get(reverse('account_reset_password_proxy') + (
        '?next=http%3A//www.example.com/test/next'
    ))
    assert response.status_code == 200


def test_account_change_password(signed_client):
    response = signed_client.get(reverse('account_change_password_proxy'))
    assert response.status_code == 302


def test_account_reset_password_done(signed_client):
    response = signed_client.get(reverse('account_reset_password_done_proxy'))
    assert response.status_code == 200


def test_account_reset_password_from_key(signed_client):
    response = signed_client.get(reverse(
        'account_reset_password_from_key_proxy',
        kwargs={'uidb36': 'asdf', 'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_sso_root_proxy(signed_client):
    response = signed_client.get(reverse('sso_root_proxy'))
    assert response.status_code == 302
