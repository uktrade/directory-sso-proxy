from django.core.urlresolvers import reverse


def test_404(client):
    response = client.get('/asdf/')
    assert response.status_code == 404


def test_account_signup(client):
    response = client.get(reverse('account_signup_proxy'))
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
    response = client.get(reverse('account_email_verification_sent_proxy'))
    assert response.status_code == 200


def test_account_confirm_email(client):
    response = client.get(reverse(
        'account_confirm_email_proxy',
        kwargs={'key': 'asdf'}
    ))
    assert response.status_code == 200


def test_account_set_password(client):
    response = client.get(reverse('account_set_password_proxy'))
    assert response.status_code == 302


def test_account_reset_password(client):
    response = client.get(reverse('account_reset_password_proxy'))
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
