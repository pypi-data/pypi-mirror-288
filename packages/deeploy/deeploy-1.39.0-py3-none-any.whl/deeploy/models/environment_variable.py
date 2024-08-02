from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class EnvironmentVariable(BaseModel):
    id: str
    name: str
    key: str
    value_encrypted: list
    workspace_id: str
    created_by: str
    last_updated_by: str
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
