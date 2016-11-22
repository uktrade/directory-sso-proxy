import pytest


def test_404(client):
    response = client.get('/asdf/')
    assert response.status_code == 404
