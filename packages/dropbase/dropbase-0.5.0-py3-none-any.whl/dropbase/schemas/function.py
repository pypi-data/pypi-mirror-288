from pydantic import BaseModel


class RunClass(BaseModel):
    app_name: str
    page_name: str
    action: str
    resource: str
    state: dict
    store: dict


class RunPythonStringRequest(BaseModel):
    app_name: str
    page_name: str
    code: str
    test: str
    state: dict
    store: dict
