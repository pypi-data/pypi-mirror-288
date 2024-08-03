import importlib
import json
from typing import Any

from pydantic import BaseModel, create_model

from dropbase.models.charts import ChartProperty
from dropbase.models.components import (
    BooleanProperty,
    ButtonProperty,
    InputProperty,
    SelectProperty,
    TextProperty,
)
from dropbase.models.table import TableProperty


def get_state_context_model(app_name: str, page_name: str, model_type: str):
    module_name = f"workspace.{app_name}.{page_name}.{model_type}"
    module = importlib.import_module(module_name)
    module = importlib.reload(module)
    return getattr(module, model_type.capitalize())


def read_page_properties(app_name: str, page_name: str):
    path = f"workspace/{app_name}/{page_name}/properties.json"
    with open(path, "r") as f:
        return json.loads(f.read())


def read_app_properties(app_name: str):
    path = f"workspace/{app_name}/properties.json"
    with open(path, "r") as f:
        return json.loads(f.read())


block_type_mapping = {
    "table": TableProperty,
    "chart": ChartProperty,
    "input": InputProperty,
    "select": SelectProperty,
    "button": ButtonProperty,
    "text": TextProperty,
    "boolean": BooleanProperty,
}


def compose_block_properties_model(properties: dict):
    blocks = {}
    for key, value in properties.get("blocks").items():
        blocks[key] = (block_type_mapping[value["type"]], ...)
    Blocks = create_model("Blocks", **blocks)
    return create_model("Properties", **{"blocks": (Blocks, ...), "store": (Any, ...)})


def get_page_properties(app_name: str, page_name: str):
    properties = read_page_properties(app_name, page_name)
    Properties = compose_block_properties_model(properties)
    # create page object
    return Properties(**properties)


def validate_page_properties(properties: dict):
    blocks = properties.get("blocks")
    for key, value in blocks.items():
        if key != value["name"]:
            raise ValueError(f"Key {key} does not match name {value['name']}")
    Properties = compose_block_properties_model(properties)
    return Properties(**properties)


def _dict_from_pydantic_model(model):
    data = {}
    for name, field in model.__fields__.items():
        if isinstance(field.outer_type_, type) and issubclass(field.outer_type_, BaseModel):
            data[name] = _dict_from_pydantic_model(field.outer_type_)
        else:
            data[name] = field.default
    return data
