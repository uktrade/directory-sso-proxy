from django.core.urlresolvers import reverse


def test_session_user_proxy(client):
    response = client.get(reverse('session_user_proxy'))
    assert response.status_code == 403
