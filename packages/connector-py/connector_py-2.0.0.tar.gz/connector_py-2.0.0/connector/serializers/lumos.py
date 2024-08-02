from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class FoundAccountData(BaseModel):
    integration_specific_id: str
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    username: Optional[str] = None
    user_status: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    custom_attributes: Optional[Dict[str, str]] = None


class CustomAttributeType(str, Enum):
    """Indicates the type of the attribute"""

    STRING = "STRING"
    USER = "USER"


class CustomAttributeCustomizedType(str, Enum):
    """Indicates the type of the entity that would own the attribue"""

    ACCOUNT = "ACCOUNT"
    ENTITLEMENMT = "ENTITLEMENT"
    RESOURCE = "RESOURCE"


class CustomAttributeSchema(BaseModel):
    customized_type: CustomAttributeCustomizedType
    name: str
    attribute_type: CustomAttributeType


class FoundResourceData(BaseModel):
    integration_specific_id: str
    label: str
    resource_type: str
    extra_data: Optional[Dict[str, Any]] = None


class FoundEntitlementData(BaseModel):
    integration_specific_id: str
    integration_specific_resource_id: str
    entitlement_type: str
    is_assignable: Optional[bool] = None
    label: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


class FoundEntitlementAssociation(BaseModel):
    integration_specific_entitlement_id: str
    account: FoundAccountData
    integration_specific_resource_id: str


class EncounteredErrorResponse(BaseModel):
    message: str
    status_code: Optional[int] = None
    error_code: Optional[str] = None
    raised_by: Optional[str] = None
    raised_in: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


Response = TypeVar("Response")


class PageCursor(BaseModel):
    next: str | None


class ResponseWrapper(BaseModel, Generic[Response]):
    response: Response
    raw_data: Optional[dict[str, Any]] = None
    cursor: PageCursor | None = None


class BaseArgs(BaseModel):
    include_raw_data: bool = Field(default=False)


class ListAccountsArgsBase(BaseArgs):
    custom_attributes: Optional[list[str]] = Field(None)


class ListCustomAttributesSchemaArgsBase(BaseArgs):
    pass


class ListCustomAttributesSchemaResp(ResponseWrapper[list[CustomAttributeSchema]]):
    pass


class ListAccountsResp(ResponseWrapper[list[FoundAccountData]]):
    pass


class ValidateCredentialsArgsBase(BaseArgs):
    pass


class ValidateCredentialsResp(ResponseWrapper[bool]):
    pass


class GetAccountArgsBase(BaseArgs):
    pass


class GetAccountResp(ResponseWrapper[FoundAccountData]):
    pass


class ListResourcesArgsBase(BaseArgs):
    resource_type: str


class ListResourcesResp(ResponseWrapper[list[FoundResourceData]]):
    pass


class GetResourceArgsBase(BaseArgs):
    resource_type: str
    integration_specific_id: str


class GetResourceResp(ResponseWrapper[FoundResourceData]):
    pass


class ListEntitlementsArgsBase(BaseArgs):
    resource_type: str
    resource_integration_specific_id: str


class ListEntitlementsResp(ResponseWrapper[list[FoundEntitlementData]]):
    pass


class FindEntitlementAssociationsArgsBase(BaseArgs):
    entitlements: List[FoundEntitlementData]


class FindEntitlementAssociationsResp(ResponseWrapper[list[FoundEntitlementAssociation]]):
    pass


class AssignEntitlementArgsBase(BaseArgs):
    account: FoundAccountData
    entitlement: FoundEntitlementData


class AssignEntitlementResp(ResponseWrapper[bool]):
    pass


class UnassignEntitlementArgsBase(BaseArgs):
    account: FoundAccountData
    entitlement: FoundEntitlementData


class UnassignEntitlementResp(ResponseWrapper[bool]):
    pass


class ErrorResp(ResponseWrapper[EncounteredErrorResponse]):
    error: bool = True
    pass
