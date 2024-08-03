import ast
import importlib
import json
import os
import sys
import time
import traceback
import uuid
from io import StringIO

import astor
from dotenv import load_dotenv

from dropbase.helpers.logger import update_dev_logs

load_dotenv()


def run(r):

    file_name = "f" + uuid.uuid4().hex + ".py"
    response = {
        "id": os.getenv("job_id"),
        "stdout": "",
        "traceback": "",
        "message": "",
        "type": "",
        "status_code": 202,
    }

    context, store_out = {}, {}

    try:
        # redirect stdout
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

        # read state and context
        state = json.loads(os.getenv("state"))
        store = json.loads(os.getenv("store"))
        code = os.getenv("code")
        test = os.getenv("test")

        # compose code
        code_str = compose_code(code, test, state, store)
        code_str = assign_last_expression(code_str)

        with open(file_name, "w") as f:
            f.write(code_str)

        # import temp file
        module_name = file_name.split(".")[0]  # this gets you "temp_file"
        module = importlib.import_module(module_name)  # this imports the module
        result = module.result  # this gets the "result" from the module

        # convert result to json
        if isinstance(result, tuple):
            if result[0].__class__.__name__ == "Context" and result[1].__class__.__name__ == "Store":
                response["type"] = "context"
                context = result[0].dict()
                store_out = result[1].dict()
                response["context"] = context
                response["store"] = store_out
            else:
                response["type"] = "generic"
                response["data"] = result
        else:
            response["type"] = "generic"
            response["data"] = result

        response["message"] = "Job completed"
        response["status_code"] = 200
    except Exception as e:
        # catch any error and tracebacks and send to rabbitmq
        response["type"] = "error"
        response["message"] = str(e)
        response["status_code"] = 500
        response["traceback"] = traceback.format_exc()
    finally:
        # get stdout
        response["stdout"] = redirected_output.getvalue()
        sys.stdout = old_stdout

        # send result to redis
        r.set(os.getenv("job_id"), json.dumps(response))
        r.expire(os.getenv("job_id"), 60)

        # remove temp file
        os.remove(file_name)

        response["completed_at"] = int(time.time())
        response["context"] = json.dumps(context, default=str, separators=(",", ":"))
        response["store"] = json.dumps(store_out, default=str, separators=(",", ":"))
        update_dev_logs(response)


def compose_code(code: str, test: str, state: dict, store: dict) -> str:
    code += f"""
from dropbase.helpers.utils import _dict_from_pydantic_model

# initialize context
context = _dict_from_pydantic_model(Context)
context = Context(**context)

# initialize state
state = State(**{state})
store = Store(**{store})
"""
    code += test
    return code


def assign_last_expression(code: str) -> str:
    """
    get test code and assign last expression to a variable named result
    """
    module = ast.parse(code)

    if module.body:
        # get the last statement
        last_statement = module.body[-1]

        # Replace Expr statement with assignment to "result"
        assign = ast.Assign(targets=[ast.Name(id="result", ctx=ast.Store())], value=last_statement.value)
        module.body[-1] = assign

    # Transform the AST back to Python code
    return astor.to_source(module)
