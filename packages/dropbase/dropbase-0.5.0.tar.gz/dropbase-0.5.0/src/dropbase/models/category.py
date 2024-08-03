from pydantic import Field


class PropertyCategory:
    default = Field(category="Default")
    view_only = Field(category="View Only")
    other = Field(category="Other")
    internal = Field(category="Internal")
