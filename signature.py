from sigauth.utils import RequestSigner, RequestSignatureChecker

from django.conf import settings


sso_signer = RequestSigner(settings.SIGNATURE_SECRET)
sso_client_checker = RequestSignatureChecker(settings.SSO_CLIENT_KEY)
