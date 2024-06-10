from django.urls import re_path, path

import core.views
import healthcheck.pingdom.views


urlpatterns = [
    re_path(
        r'pingdom/ping.xml',
        healthcheck.pingdom.views.PingDomView.as_view(),
        name='pingdom',
    ),
    re_path(r'', core.views.ProxyView.as_view()),
]

