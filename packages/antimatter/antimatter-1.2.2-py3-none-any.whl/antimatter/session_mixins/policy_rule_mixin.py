from typing import Any, Callable, Dict, List, Optional, Union

import antimatter_api as openapi_client
from antimatter.constants import domain_policy
from antimatter.builders.capability import CapabilityRulesBuilder
from antimatter.builders.fact_policy import FactPoliciesBuilder

from antimatter.session_mixins.base import BaseMixin


class PolicyRuleMixin(BaseMixin):
    """
    Session mixin defining policy rule CRUD functionality.
    """

    def create_policy_rule(
        self,
        capability_rules: CapabilityRulesBuilder,
        path: str,
        operation: Union[str, domain_policy.Operation],
        result: Union[str, domain_policy.Result],
        priority: int = 0,
        facts: Optional[FactPoliciesBuilder] = None,
        disabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a policy rule for the domain.

        :param capability_rules: Rules referring to domain identity capabilities. These rules are ANDed together
        :param facts: Assert the existence or nonexistence of facts that reference the capability rules.
                    These assertions will be ANDed together, and ANDed with the capability rules.
        :param path: The path this rule governs. May contain glob expressions (e.g. '*' and '**')
        :param operation: The operation to apply the policy to
        :param result: Whether to 'allow' or 'deny' the operation performed that matches this rule
        :param priority: The priority of this rule. Lower priority rules are evaluated first
        :param disabled: If this rule is disabled or not
        :return: A dictionary containing the created rule from the server
        """
        res = openapi_client.PolicyApi(self.authz.get_client()).domain_create_policy_rule(
            domain_id=self.domain_id,
            new_domain_policy_rule=openapi_client.NewDomainPolicyRule(
                domain_identity=capability_rules.build() if capability_rules is not None else None,
                facts=facts.build() if facts is not None else [],
                path=path,
                operation=domain_policy.Operation(operation).value,
                result=domain_policy.Result(result).value,
                priority=priority,
                disabled=disabled,
            ),
        )
        policy_rule = res.model_dump()
        return policy_rule

    def delete_policy_rule(self, rule_id: str):
        """
        Delete a domain policy rule on the session's domain.

        :param rule_id: Identifier of the policy rule to delete
        """
        openapi_client.PolicyApi(self.authz.get_client()).domain_delete_policy_rule(
            domain_id=self.domain_id, rule_id=rule_id
        )

    def list_policy_rules(self):
        """
        Get the domain's policy rules.

        :return: A list of policy rules.
        """
        res = openapi_client.PolicyApi(self.authz.get_client()).domain_list_policy_rules(
            domain_id=self.domain_id
        )
        policy_rules = []
        for rule in res.rules:
            policy_rules.append(rule.model_dump())
        return policy_rules

    def update_policy_rule(
        self,
        rule_id: str,
        capability_rules: CapabilityRulesBuilder,
        facts: FactPoliciesBuilder,
        path: str,
        operation: Union[str, domain_policy.Operation],
        result: Union[str, domain_policy.Result],
        priority: int,
        disabled: bool = False,
    ) -> None:
        """
        Update a domain policy rule by ID.

        :param rule_id: The ID of the rule to update
        :param capability_rules: Rules referring to domain identity capabilities. These rules are ANDed together
        :param facts: Assert the existence or nonexistence of facts that reference the capability rules.
                    These assertions will be ANDed together, and ANDed with the capability rules.
        :param path: The path this rule governs. May contain glob expressions (e.g. '*' and '**')
        :param operation: The operation to apply the policy to
        :param result: Whether to 'allow' or 'deny' the operation performed that matches this rule
        :param priority: The priority of this rule. Lower priority rules are evaluated first
        :param disabled: If this rule is disabled or not
        """
        openapi_client.PolicyApi(self.authz.get_client()).domain_update_policy_rule(
            domain_id=self.domain_id,
            rule_id=rule_id,
            new_domain_policy_rule=openapi_client.NewDomainPolicyRule(
                domain_identity=capability_rules.build() if capability_rules is not None else None,
                facts=facts.build() if facts is not None else None,
                path=path,
                operation=domain_policy.Operation(operation).value,
                result=domain_policy.Result(result).value,
                priority=priority,
                disabled=disabled,
            ),
        )

    def renumber_policy_rules(self) -> List[Dict[str, Any]]:
        """
        Re-assign rule priority numbers for the session's domain to integer multiples of 10

        :return: The full list of renumbered policy rules in this domain
        """
        res = openapi_client.PolicyApi(self.authz.get_client()).domain_renumber_policy_rules(
            domain_id=self.domain_id
        )
        policy_rules = []
        for rule in res.rules:
            policy_rules.append(rule.model_dump())
        return policy_rules
