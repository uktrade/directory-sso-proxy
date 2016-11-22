from django.core.urlresolvers import reverse


def test_health_check_proxy(client):
    response = client.get(reverse('health_check_proxy'))
    assert response.status_code == 200
