from typing import Dict, Optional, Union

from pydantic import BaseModel, Field

from dropbase.models.charts import ChartProperty
from dropbase.models.components import (
    BooleanProperty,
    ButtonProperty,
    InputProperty,
    SelectProperty,
    TextProperty,
)
from dropbase.models.table import TableProperty

BlockType = Optional[
    Union[
        TableProperty,
        ChartProperty,
        BooleanProperty,
        ButtonProperty,
        InputProperty,
        SelectProperty,
        TextProperty,
    ]
]


class PageProperty(BaseModel):
    blocks: Dict[str, BlockType] = Field(default_factory=dict)
    store: Dict = Field(default_factory=dict)
