from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory


class ChartContextProperty(BaseModel):
    data: Optional[Any]
    message: Optional[str]
    message_type: Optional[str]


class ChartProperty(BaseComponent):
    # general
    type: Literal["chart"]
    description: Annotated[Optional[str], PropertyCategory.default]
    refetch_interval: Annotated[Optional[int], PropertyCategory.default]

    # internal
    context: ModelMetaclass = ChartContextProperty
