from typing import Annotated, Any, Literal, Optional

from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory
from dropbase.models.common import ComponentProperty

data_type_options = Literal["text", "integer", "float", "datetime", "date", "time"]


class InputProperty(BaseComponent):
    type: Literal["input"]

    # general
    data_type: Annotated[data_type_options, PropertyCategory.default]
    placeholder: Annotated[Optional[str], PropertyCategory.default]
    default: Annotated[Optional[Any], PropertyCategory.default]
    multiline: Annotated[Optional[bool], PropertyCategory.default] = False

    # internal
    context: ModelMetaclass = ComponentProperty

    def __init__(self, **data):
        data.setdefault("data_type", "text")
        super().__init__(**data)
