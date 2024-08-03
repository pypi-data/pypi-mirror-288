from typing import Annotated, Optional

from pydantic import BaseModel

from dropbase.models.category import PropertyCategory


class BaseComponent(BaseModel):

    # general
    name: Annotated[str, PropertyCategory.default]
    label: Annotated[str, PropertyCategory.default]

    # position
    w: Annotated[Optional[int], PropertyCategory.internal] = 2
    h: Annotated[Optional[int], PropertyCategory.internal] = 1
    x: Annotated[Optional[int], PropertyCategory.internal] = 0
    y: Annotated[Optional[int], PropertyCategory.internal] = 0
