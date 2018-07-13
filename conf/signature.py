from sigauth.utils import RequestSigner, RequestSignatureChecker

from django.conf import settings


sso_signer = RequestSigner(settings.SSO_SIGNATURE_SECRET)
sso_client_checker = RequestSignatureChecker(settings.SIGNATURE_SECRET)
