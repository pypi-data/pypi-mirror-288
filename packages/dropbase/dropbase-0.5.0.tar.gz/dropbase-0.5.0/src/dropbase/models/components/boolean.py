from typing import Annotated, Any, Literal, Optional

from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory
from dropbase.models.common import ComponentProperty


class BooleanProperty(BaseComponent):
    type: Literal["boolean"]
    default: Annotated[Optional[Any], PropertyCategory.default] = False

    data_type: Literal["boolean"] = "boolean"
    # internal
    context: ModelMetaclass = ComponentProperty
