from pydantic import BaseModel, Field, Json


class EmptyModel(BaseModel):
    pass


class CommandTypes(BaseModel):
    argument: Json = Field(..., description="OpenAPI Component")
    output: Json = Field(..., description="OpenAPI Component")


class Info(BaseModel):
    app_id: str
    capabilities: list[str]
    capability_schema: dict[str, CommandTypes]
