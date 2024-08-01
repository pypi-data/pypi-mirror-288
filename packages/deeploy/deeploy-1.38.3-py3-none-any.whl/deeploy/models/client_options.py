from typing import Optional

from pydantic import BaseModel


class ClientConfig(BaseModel):
    """
    Class containing the Deeploy client options

    Attributes:
      host: string representing the domain on which Deeploy is hosted
      workspace_id: string representing the workspace id in which to create
        deployments
      access_key: string representing the personal access key
      secret_key: string representing the personal secret key
      token: string representing the Deployment token
    """

    host: Optional[str]
    workspace_id: Optional[str]
    access_key: Optional[str]
    secret_key: Optional[str]
    token: Optional[str]
