from connector.sync_.lumos import LumosCommandsMixin
from connector.serializers.lumos import (
    AssignEntitlementResp,
    FindEntitlementAssociationsResp,
    FoundAccountData,
    FoundEntitlementData,
    FoundResourceData,
    ListAccountsResp,
    ListEntitlementsResp,
    ListResourcesResp,
    UnassignEntitlementResp,
    ValidateCredentialsResp,
    ListCustomAttributesSchemaArgsBase,
    ListCustomAttributesSchemaResp,
)

from {name}.serializers.lumos import (
    AssignEntitlementArgs,
    FindEntitlementAssociationsArgs,
    ListAccountsArgs,
    ListEntitlementsArgs,
    ListResourcesArgs,
    UnassignEntitlementArgs,
    ValidateCredentialsArgs,
)


class SyncCommands(LumosCommandsMixin):
    app_id = "{hyphenated_name}"

    def validate_credentials(self, args: ValidateCredentialsArgs) -> ValidateCredentialsResp:
        return ValidateCredentialsResp(
            response=True,
            errors=[],
            raw_data={{}},
        )

    def list_accounts(self, args: ListAccountsArgs) -> ListAccountsResp:
        return ListAccountsResp(
            response=[FoundAccountData(given_name="{title}", integration_specific_id="100", email="albus@lumos.com")],
            errors=[],
            raw_data = {{"localhost:8080/test": {{"test": "test"}}}},
        )

    def list_resources(self, args: ListResourcesArgs) -> ListResourcesResp:
        return ListResourcesResp(
            response={{
                "MOCK_CONNECTOR_RESOURCE_1": [
                    FoundResourceData(
                        integration_specific_id="1234",
                        label="Starter Resource",
                        resource_type="MOCK_CONNECTOR_RESOURCE_1",
                    )
                ]
            }},
            errors=[],
            raw_data={{}},
        )

    def list_entitlements(self, args: ListEntitlementsArgs) -> ListEntitlementsResp:
        return [
            FoundEntitlementData(
                integration_specific_id="1234",
                integration_specific_resource_id="1234",
                is_assignable=False,
                label="mock entitlement",
                entitlement_type="MOCK_CONNECTOR_ENTITLEMENT_1",
            )
        ]

    def find_entitlement_associations(
        self,
        args: FindEntitlementAssociationsArgs,
    ) -> FindEntitlementAssociationsResp:
        return []

    def assign_entitlement(
        self,
        args: AssignEntitlementArgs,
    ) -> AssignEntitlementResp:
        pass

    def unassign_entitlement(
        self,
        args: UnassignEntitlementArgs,
    ) -> UnassignEntitlementResp:
        pass

    def list_custom_attributes_schema(
        self, args: ListCustomAttributesSchemaArgsBase
    ) -> ListCustomAttributesSchemaResp:
        return []
