from django.urls import reverse


def test_pingdom_app_healthcheck_ok(client):
    response = client.get(reverse('pingdom'))
    assert response.status_code == 302
