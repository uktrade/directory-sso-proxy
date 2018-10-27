from django.conf.urls import url, include
from django.conf import settings

import conf.urls
import proxy.utils


urlpatterns = [
    url(
        r'^sso/',
        include(conf.urls.urlpatterns)
    )
]


if settings.DEBUG:
    urlpatterns += [
        url(
            r'^static/',
            proxy.utils.StaticProxyView.as_view(),
            name='unprefoxed-static-proxy'
        ),
    ]
