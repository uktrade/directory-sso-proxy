from django.conf import settings
from sigauth.helpers import RequestSigner

sso_signer = RequestSigner(settings.SSO_SIGNATURE_SECRET, sender_id='directory')
