from django.conf.urls import url

import core.views

urlpatterns = [url(r'', core.views.ProxyView.as_view())]
