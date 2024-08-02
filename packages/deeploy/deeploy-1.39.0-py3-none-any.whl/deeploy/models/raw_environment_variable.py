from typing import List

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class RawEnvironmentVariable(BaseModel):
    id: str
    name: str
    key: str
    value: str
    used_in: List[str]
    workspace_id: str
    created_by: str
    last_updated_by: str
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
