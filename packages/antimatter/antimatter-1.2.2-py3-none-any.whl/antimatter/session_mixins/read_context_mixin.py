from typing import Any, Callable, Dict, List

import antimatter_api as openapi_client
from antimatter.builders import ReadContextBuilder, ReadContextRuleBuilder

from antimatter.session_mixins.base import BaseMixin


class ReadContextMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for read contexts.
    """

    def add_read_context(self, name: str, builder: ReadContextBuilder) -> None:
        """
        Upserts a read context for the current domain and auth

        :param name: The name of the read context to add or update
        :param builder: The builder containing read context configuration
        """
        if builder is None:
            raise ValueError("Read context builder is required")
        openapi_client.ContextsApi(self.authz.get_client()).domain_upsert_read_context(
            domain_id=self.domain_id,
            context_name=name,
            add_read_context=builder.build(),
        )

    def list_read_context(self) -> List[Dict[str, Any]]:
        """
        Returns a list of read contexts available for the current domain and auth
        """
        return [
            ctx.model_dump()
            for ctx in openapi_client.ContextsApi(self.authz.get_client())
            .domain_list_read_contexts(self.domain_id)
            .read_contexts
        ]

    def describe_read_context(self, name: str) -> Dict[str, Any]:
        """
        Returns the read context with the given name for the current domain and auth

        :param name: The name of the read context to describe
        :return: The full details of the read context
        """
        return (
            openapi_client.ContextsApi(self.authz.get_client())
            .domain_get_read_context(self.domain_id, context_name=name)
            .model_dump()
        )

    def delete_read_context(self, name: str) -> None:
        """
        Delete a read context. All configuration associated with this read
        context will also be deleted. Domain policy rules referencing this read
        context will be left as-is.

        :param name: The name of the read context to delete
        """
        openapi_client.ContextsApi(self.authz.get_client()).domain_delete_read_context(
            domain_id=self.domain_id, context_name=name
        )

    def list_read_context_rules(self, name: str) -> List[Dict[str, Any]]:
        """
        List all rules for the read context

        :param name: The name of the read context to list rules from
        :return: The list of read context rules
        """
        return [
            r.model_dump()
            for r in openapi_client.ContextsApi(self.authz.get_client())
            .domain_get_read_context(self.domain_id, context_name=name)
            .rules
        ]

    def add_read_context_rules(
        self,
        name: str,
        rule_builder: ReadContextRuleBuilder,
    ) -> str:
        """
        Adds rules to a read context

        :param name: The name of the read context to add rules to
        :param rule_builder: The builder containing rule configuration for the read context
        :return: The unique ID for the added read context rule
        """
        if rule_builder is None:
            raise ValueError("Read context rule builder is required")
        return (
            openapi_client.ContextsApi(self.authz.get_client())
            .domain_add_read_context_rule(
                domain_id=self.domain_id,
                context_name=name,
                new_read_context_config_rule=rule_builder.build(),
            )
            .id
        )

    def update_read_context_rule(
        self,
        name: str,
        rule_id: str,
        rule_builder: ReadContextRuleBuilder,
    ) -> None:
        """
        Update a read context configuration rule. The rule must already exist.

        :param name: The name of the read context to update a rule for
        :param rule_id: The unique ID of the rule to update
        :param rule_builder: The builder containing rule configuration
        """
        if rule_builder is None:
            raise ValueError("Read context rule builder is required")
        openapi_client.ContextsApi(self.authz.get_client()).domain_update_read_context_rule(
            domain_id=self.domain_id,
            context_name=name,
            rule_id=rule_id,
            new_read_context_config_rule=rule_builder.build(),
        )

    def delete_read_context_rule(
        self,
        name: str,
        rule_id: str,
    ) -> None:
        """
        Deletes a rule from a read context

        :param name: The name of the read context to delete a rule from
        :param rule_id: The unique ID of the rule to delete
        """
        openapi_client.ContextsApi(self.authz.get_client()).domain_delete_read_context_rule(
            domain_id=self.domain_id,
            context_name=name,
            rule_id=rule_id,
        )

    def delete_read_context_rules(self, name: str) -> None:
        """
        Deletes all the read context rules

        :param name: The name of the read context to delete all the rules from
        """
        for rule in self.list_read_context_rules(name):
            openapi_client.ContextsApi(self.authz.get_client()).domain_delete_read_context_rule(
                domain_id=self.domain_id,
                context_name=name,
                rule_id=rule["id"],
            )

    def flush_read_context(self, name: str) -> None:
        """
        Flushes the read context and all associated rules

        :param name: The name of the read context to flush
        """
        contexts_api = openapi_client.ContextsApi(api_client=self.authz.get_client())
        contexts_api.domain_read_context_flush(domain_id=self.domain_id, context_name=name)
