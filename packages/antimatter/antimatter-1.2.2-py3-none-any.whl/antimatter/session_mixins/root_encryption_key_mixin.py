from typing import Any, Callable, Dict, List

import antimatter_api as openapi_client
from antimatter_api import KeyInfos, ActiveRootEncryptionKeyID

from antimatter.session_mixins.base import BaseMixin


class RootEncryptionKeyMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for root encryption keys
    """

    def get_active_root_encryption_key(self) -> Dict[str, Any]:
        """
        Get the active root encryption key

        :return: The active root encryption key
        """
        return (
            openapi_client.EncryptionApi(self.authz.get_client())
            .domain_get_active_external_root_encryption_key(domain_id=self.domain_id)
            .model_dump()
        )

    def list_root_encryption_keys(self) -> List[Dict[str, Any]]:
        """
        List all root encryption keys

        :return: A list of root encryption keys
        """
        return [
            key.model_dump()
            for key in openapi_client.EncryptionApi(
                self.authz.get_client()
            ).domain_list_external_root_encryption_key(domain_id=self.domain_id)
        ]

    def test_root_encryption_key(self, root_encryption_key_id: str) -> Dict[str, Any]:
        """
        Attempt to test a root encryption key to encrypt and decrypt

        :param key: The key to test
        :return: The result of the test
        """
        return (
            openapi_client.EncryptionApi(self.authz.get_client())
            .domain_external_root_encryption_key_test(
                domain_id=self.domain_id, root_encryption_key_id=root_encryption_key_id, body={}
            )
            .model_dump()
        )

    def add_root_encryption_key(self, key_infos: KeyInfos, description: str = "") -> str:
        """
        Add a new root encryption key.
        Use the builder functions in `antimatter.builders.root_encryption_key` to create the key information.

        For example:

        .. code-block:: python

            key_info = antimatter.builders.antimatter_delegated_aws_key_info(key_arn="key_arn")
            key_id = session.add_root_encryption_key(key_info)

            key_info = antimatter.builders.aws_service_account_key_info(
                access_key_id="access_key_id", secret_access_key
            )
            key_id = session.add_root_encryption_key(key_info)

            key_info = antimatter.builders.gcp_service_account_key_info(
                service_account_credentials="service_account_credentials", project_id="project_id", location="location"
            )
            key_id = session.add_root_encryption_key(key_info)

        :param key_infos: The key information to add
        :param description: The description of the key
        """
        assert key_infos is not None, "Key information is required"

        key_infos.description = description
        return (
            openapi_client.EncryptionApi(self.authz.get_client())
            .domain_add_external_root_encryption_key(domain_id=self.domain_id, key_infos=key_infos)
            .rek_id
        )

    def delete_root_encryption_key(self, root_encryption_key_id: str):
        """
        Delete a root encryption key. Only possible if key is not in use by any data key encryption keys

        :param key: The key to delete
        """
        openapi_client.EncryptionApi(self.authz.get_client()).domain_delete_external_root_encryption_key(
            domain_id=self.domain_id, root_encryption_key_id=root_encryption_key_id
        )

    def set_active_root_encryption_key(self, root_encryption_key_id: str) -> None:
        """
        Set the active root encryption key for the domain

        :param key: The key to set as active
        """
        openapi_client.EncryptionApi(self.authz.get_client()).domain_set_active_external_root_encryption_key(
            domain_id=self.domain_id,
            active_root_encryption_key_id=openapi_client.ActiveRootEncryptionKeyID(
                key_id=root_encryption_key_id
            ),
        )

    def rotate_encryption_keys(self) -> None:
        """
        Rotates the root encryption keys. This is a batched operation and if 'True' is
        returned, this indicates whether there are more key encryption keys that can be rotated.
        """
        return (
            openapi_client.EncryptionApi(self.authz.get_client())
            .domain_rotate_root_encryption_keys(
                domain_id=self.domain_id,
                body={},
            )
            .has_more
        )

    def list_key_providers(self) -> List[Dict[str, Any]]:
        """
        Retrieve the domain's key providers and a brief overview of their
        configuration.
        """
        res = openapi_client.EncryptionApi(
            self.authz.get_client()
        ).domain_get_external_root_encryption_key_providers(domain_id=self.domain_id)
        if not res.providers:
            return []
        return [
            provider.actual_instance.model_dump()
            for provider in res.providers
            if provider.actual_instance is not None
        ]
