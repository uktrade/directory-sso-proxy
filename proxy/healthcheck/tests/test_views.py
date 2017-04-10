from django.core.urlresolvers import reverse


def test_health_check_proxy(signed_client):
    response = signed_client.get(reverse('health_check_proxy'))
    assert response.status_code == 200
