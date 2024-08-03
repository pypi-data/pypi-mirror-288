from typing import Annotated, Any, Dict, List, Literal, Optional

from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory
from dropbase.models.common import ComponentProperty


class SelectContextProperty(ComponentProperty):
    options: Annotated[Optional[List[Dict]], PropertyCategory.default]


class SelectOptions(BaseModel):
    id: Optional[str]
    label: str
    value: Any


data_type_options = Literal["string", "integer", "float", "boolean", "string_array"]


class SelectProperty(BaseComponent):
    type: Literal["select"]
    data_type: Annotated[data_type_options, PropertyCategory.default]
    options: Annotated[Optional[List[SelectOptions]], PropertyCategory.default]
    default: Annotated[Optional[Any], PropertyCategory.other]
    multiple: Annotated[Optional[bool], PropertyCategory.other] = False

    # internal
    context: ModelMetaclass = SelectContextProperty

    def __init__(self, **data):
        data.setdefault("data_type", "string")
        super().__init__(**data)
