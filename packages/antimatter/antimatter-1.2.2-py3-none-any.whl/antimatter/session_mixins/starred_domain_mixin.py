from typing import Any, Dict, List

import antimatter_api as openapi_client
from antimatter import errors

from antimatter.session_mixins.base import BaseMixin


class StarredDomainMixin(BaseMixin):

    def _verify_call(self):
        if self.authz.auth_client.get_token_scope() != "google_oauth_token":
            raise errors.PermissionDenied("use an oauth client to access this functionality")
        return

    def list_starred_domains(self) -> List[Dict[str, Any]]:
        """
        Returns a list of starred domains for the current user
        """
        self._verify_call()
        return [
            domain
            for domain in openapi_client.AccountManagementApi(self.authz.get_client())
            .starred_domain_list()
            .domains
        ]

    def add_starred_domain(self, domain_id: str) -> None:
        """
        Adds a domain to the starred list for the current user
        """
        self._verify_call()
        openapi_client.AccountManagementApi(self.authz.get_client()).starred_domain_add(domain_id=domain_id)

    def delete_starred_domain(self, domain_id: str) -> None:
        """
        Removes a domain from the starred list for the current user
        """
        self._verify_call()
        openapi_client.AccountManagementApi(self.authz.get_client()).starred_domain_remove(
            domain_id=domain_id
        )
