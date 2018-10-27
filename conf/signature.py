from sigauth.helpers import RequestSigner

from django.conf import settings


sso_signer = RequestSigner(
    settings.SSO_SIGNATURE_SECRET,
    sender_id='directory',
)
