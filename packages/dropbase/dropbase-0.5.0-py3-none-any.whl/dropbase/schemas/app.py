from typing import Optional

from pydantic import BaseModel


class CreateAppRequest(BaseModel):
    app_label: str
    app_name: str


class UpdateAppRequest(BaseModel):
    app_name: str
    app_label: str
    icon: Optional[str]
