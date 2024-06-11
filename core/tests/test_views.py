import json
from unittest import mock

import pytest
import revproxy
import revproxy.views
import urllib3.response
from django.test.client import Client

from core.views import ProxyView


@pytest.fixture
def no_remote_addr_client():
    # The django test client _always_ populates REMOTE_ADDR
    # However, in production this depends on the web-server
    # environment, and we want to test the case when it's not
    # set.
    class NoRemoteAddrClient(Client):
        def _base_environ(self, **request):
            return {key: value for key, value in super()._base_environ(**request).items() if key != 'REMOTE_ADDR'}

    return NoRemoteAddrClient()


@pytest.fixture()
def mock_response():
    return urllib3.response.HTTPResponse(
        body=json.dumps({'key': 'value'}),
        headers={'Content-Type': 'application/json', 'Content-Length': '2'},
        status=200,
    )


@pytest.mark.skip(reason="TOFIX")
@pytest.mark.parametrize(
    'get_kwargs',
    (
        # If neither X-Forwarded-For nor REMOTE_ADDR, then don't set
        # X-Forwarded-For outgoing
        {},
        {'REMOTE_ADDR': '4.3.2.1'},
        # If only X-Forwarded-For incomding, then don't set
        # X-Forwarded-For outgoing
        {'HTTP_X_FORWARDED_FOR': '1.2.3.4'},
    ),
)
@mock.patch('urllib3.poolmanager.PoolManager.urlopen')
def test_x_forwarded_for_not_set(mock_urlopen, no_remote_addr_client, get_kwargs, settings, mock_response):
    settings.FEATURE_URL_PREFIX_ENABLED = True
    mock_urlopen.return_value = mock_response

    stub = mock.patch('revproxy.views.HTTP_POOLS', wraps=revproxy.views.HTTP_POOLS)
    with stub as mock_pool_manager:
        no_remote_addr_client.get('/sso/accounts/login/', **get_kwargs)
    headers = mock_pool_manager.urlopen.call_args[1]['headers']
    assert 'X-Forwarded-For' not in headers


@pytest.mark.skip(reason="TOFIX")
@mock.patch('urllib3.poolmanager.PoolManager.urlopen')
def test_if_x_forwarded_for_and_remote_addr_then_are_concat_with_comma(mock_urlopen, client, settings, mock_response):
    settings.FEATURE_URL_PREFIX_ENABLED = False
    mock_urlopen.return_value = mock_response

    stub = mock.patch('revproxy.views.HTTP_POOLS', wraps=revproxy.views.HTTP_POOLS)
    with stub as mock_pool_manager:
        client.get('/sso/accounts/login/', REMOTE_ADDR='4.3.2.1', HTTP_X_FORWARDED_FOR='1.2.3.4')

    headers = mock_pool_manager.urlopen.call_args[1]['headers']
    assert headers['X-Forwarded-For'] == '1.2.3.4, 4.3.2.1'


@mock.patch('core.views.ProxyView.get_upstream')
@mock.patch('urllib3.poolmanager.PoolManager.urlopen')
def test_get_upstream_response_http_error_logged_and_raised(
    mock_urlopen, mock_get_upstream, caplog, client, rf, settings, mock_response
):
    mock_urlopen.side_effect = urllib3.exceptions.HTTPError("Fake problem")
    mock_get_upstream.return_value = "https://example.com/fake/path"

    fake_request = rf.get('/sso/test/path')
    view = ProxyView()
    view.request_headers = {}

    with pytest.raises(urllib3.exceptions.HTTPError) as ctx:
        view.get_upstream_response(fake_request)

    assert 'Fake problem' in caplog.text
    assert str(ctx.value) == 'Fake problem'
