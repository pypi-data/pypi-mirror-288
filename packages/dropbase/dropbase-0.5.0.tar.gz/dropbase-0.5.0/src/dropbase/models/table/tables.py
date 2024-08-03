from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from dropbase.models.base import BaseComponent
from dropbase.models.category import PropertyCategory
from dropbase.models.table.button_column import ButtonColumnProperty
from dropbase.models.table.py_column import PyColumnProperty


class TableColumn(BaseModel):
    name: str
    column_type: str
    data_type: str
    display_type: str


class TableData(BaseModel):
    type: Optional[Literal["python"]]
    columns: Optional[List[TableColumn]]
    data: Optional[List[List[Any]]]


class TableContextProperty(BaseModel):
    data: Optional[TableData]
    message: Optional[str]
    message_type: Optional[str]


class TableProperty(BaseComponent):
    # general
    type: Literal["table"]
    description: Annotated[Optional[str], PropertyCategory.default]
    refetch_interval: Annotated[Optional[int], PropertyCategory.default]

    # children
    columns: Annotated[List[Union[PyColumnProperty, ButtonColumnProperty]], PropertyCategory.default]

    # internal
    context: ModelMetaclass = TableContextProperty
