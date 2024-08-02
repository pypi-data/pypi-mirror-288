from pydantic import Field

from connector.serializers.lumos import (
    AssignEntitlementArgsBase,
    FindEntitlementAssociationsArgsBase,
    GetAccountArgsBase,
    GetResourceArgsBase,
    ListAccountsArgsBase,
    ListEntitlementsArgsBase,
    ListResourcesArgsBase,
    UnassignEntitlementArgsBase,
    ValidateCredentialsArgsBase,
)

from .auth import Auth


class ListAccountsArgs(Auth, ListAccountsArgsBase):
    page: int
    size: int = Field(5)


class ValidateCredentialsArgs(Auth, ValidateCredentialsArgsBase):
    pass


class GetAccountArgs(Auth, GetAccountArgsBase):
    account_id: int


class ListResourcesArgs(Auth, ListResourcesArgsBase):
    page: int
    size: int = Field(5)


class GetResourceArgs(Auth, GetResourceArgsBase):
    pass


class ListEntitlementsArgs(Auth, ListEntitlementsArgsBase):
    page: int
    size: int = Field(5)


class FindEntitlementAssociationsArgs(Auth, FindEntitlementAssociationsArgsBase):
    pass


class AssignEntitlementArgs(Auth, AssignEntitlementArgsBase):
    pass


class UnassignEntitlementArgs(Auth, UnassignEntitlementArgsBase):
    pass
