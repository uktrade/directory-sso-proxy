from core import middleware


def test_prefix_url_middleware_static(rf, settings):
    request = rf.get('/static/thing')
    settings.FEATURE_URL_PREFIX_ENABLED = True

    response = middleware.PrefixUrlMiddleware().process_request(request)

    assert response is None
