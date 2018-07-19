from sigauth.utils import RequestSigner

from django.conf import settings


sso_signer = RequestSigner(settings.SSO_SIGNATURE_SECRET)
