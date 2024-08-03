from typing import Annotated, Literal, Optional

from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory
from dropbase.models.common import ComponentProperty


class TextContextProperty(ComponentProperty):
    text: Optional[str]


class TextProperty(BaseComponent):
    type: Literal["text"]
    text: Annotated[str, PropertyCategory.default]

    # internal
    context: ModelMetaclass = TextContextProperty
