from typing import Optional

import antimatter_api as openapi_client

from antimatter.authn import Unauthenticated
from antimatter.authz import TokenAuthorization
from antimatter import errors
from antimatter.session_mixins.base import BaseMixin


class VerificationMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for verification actions.
    """

    def resend_verification_email(self, email: Optional[str] = None):
        """
        Resend the verification email to the admin contact email. If the session
        was called with an email, that will be used if none is provided.

        :param email: The email to resend the verification email for.
        """
        if not email and not self.authz.auth_client.get_email():
            raise errors.SessionVerificationPendingError("unable to resend verification email: email unknown")

        # If we're trying to resend the verification email, there's no sense in using the auth
        # client - trying to authenticate will fail here if a verification email needs to be
        # sent.
        authz = TokenAuthorization(
            auth_client=Unauthenticated(enable_retries=self.authz.auth_client.has_client_retry_policy())
        )

        openapi_client.AuthenticationApi(authz.get_client()).domain_contact_issue_verify(
            domain_id=self.domain_id,
            domain_contact_issue_verify_request=openapi_client.DomainContactIssueVerifyRequest(
                admin_email=email or self.authz.auth_client.get_email(),
            ),
        )
