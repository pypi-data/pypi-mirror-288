import importlib
import json
import os
import sys
import time
import traceback
from io import StringIO

from dotenv import load_dotenv

from dropbase.helpers.logger import update_dev_logs
from dropbase.helpers.utils import _dict_from_pydantic_model

load_dotenv()


def run(r):

    response = {
        "id": os.getenv("job_id"),
        "stdout": "",
        "traceback": "",
        "message": "",
        "type": "",
        "status_code": 202,
    }
    new_context, new_store = {}, {}

    try:

        # redirect stdout
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

        # read state and context
        app_name = os.getenv("app_name")
        page_name = os.getenv("page_name")

        # get page module
        page_path = f"workspace.{app_name}.{page_name}"
        state_context_module = importlib.import_module(page_path)

        # initialize context
        Context = getattr(state_context_module, "Context")
        context = _dict_from_pydantic_model(Context)
        context = Context(**context)

        # initialize state
        state = json.loads(os.getenv("state"))
        State = getattr(state_context_module, "State")
        state = State(**state)

        # initialize store
        store = json.loads(os.getenv("store"))
        Store = getattr(state_context_module, "Store")
        store = Store(**store)

        # initialize page script
        script_path = f"workspace.{app_name}.{page_name}.script"
        page_module = importlib.import_module(script_path)
        importlib.reload(page_module)
        Script = getattr(page_module, "Script")
        script = Script(app_name, page_name)

        # get function specific variables
        action = os.getenv("action")
        resource = os.getenv("resource")

        out_context, out_store = script.__getattribute__(resource).__getattribute__(action)(
            state, context, store
        )

        # convert result to dict
        new_context = out_context.dict()
        new_store = out_store.dict()

        response["type"] = "context"
        response["message"] = "Job completed"
        response["status_code"] = 200
        response["context"] = new_context
        response["store"] = new_store
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

        # log to dev logs
        response["completed_at"] = int(time.time())
        response["context"] = json.dumps(new_context, default=str, separators=(",", ":"))
        response["store"] = json.dumps(new_store, default=str, separators=(",", ":"))
        update_dev_logs(response)
