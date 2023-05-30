from django.urls import re_path

import core.views

urlpatterns = [re_path(r'', core.views.ProxyView.as_view())]
