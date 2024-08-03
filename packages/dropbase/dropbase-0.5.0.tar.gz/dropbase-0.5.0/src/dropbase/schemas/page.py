from typing import List, Optional, Union

from pydantic import BaseModel

from dropbase.models.table import ButtonColumnProperty, PyColumnProperty, TableProperty


class TableProperties(TableProperty):
    columns: List[Optional[Union[PyColumnProperty, ButtonColumnProperty]]] = []


class PageProperties(BaseModel):
    app_name: str
    page_name: str
    properties: dict


class CreateRenamePageRequest(BaseModel):
    app_name: str
    page_name: str
    page_label: str


class SaveTableColumns(BaseModel):
    app_name: str
    page_name: str
    table_name: str
    columns: list
