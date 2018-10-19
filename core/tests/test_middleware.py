from core import middleware


def test_prefix_url_middleware_feature_off(rf, settings):
    request = rf.get('/')
    settings.FEATURE_URL_PREFIX_ENABLED = False

    response = middleware.PrefixUrlMixin().process_request(request)

    assert response is None


def test_prefix_url_middleware_not_starts_with_url_unknown_url(rf, settings):
    request = rf.get('/some-unknown-url/')
    settings.FEATURE_URL_PREFIX_ENABLED = True

    response = middleware.PrefixUrlMixin().process_request(request)

    assert response is None


def test_prefix_url_middleware_not_starts_with_url_known_url(rf, settings):
    settings.ROOT_URLCONF = 'conf.urls'
    settings.FEATURE_URL_PREFIX_ENABLED = True

    request = rf.get('/accounts/login/')

    response = middleware.PrefixUrlMixin().process_request(request)

    assert response.status_code == 302
    assert response.url == '/sso/accounts/login/'
