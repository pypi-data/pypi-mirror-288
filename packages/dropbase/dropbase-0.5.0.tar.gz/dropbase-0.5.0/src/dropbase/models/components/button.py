from typing import Annotated, Literal, Optional

from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory
from dropbase.models.common import ComponentProperty

color_options = Literal["red", "blue", "green", "yellow", "gray", "orange", "purple", "pink"]


class ButtonProperty(BaseComponent):
    type: Literal["button"]
    color: Annotated[Optional[color_options], PropertyCategory.default] = "blue"

    # internal
    context: ModelMetaclass = ComponentProperty
