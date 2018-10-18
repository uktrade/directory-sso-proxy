from django.conf.urls import url, include

import conf.urls_unprefixed


urlpatterns = [
    url(
        r'^sso/',
        include(conf.urls_unprefixed.urlpatterns)
    )
]
