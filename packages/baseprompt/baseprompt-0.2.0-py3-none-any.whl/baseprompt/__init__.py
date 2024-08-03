# __all__ = ["Baseprompt"]
from .client import Baseprompt

def run_workflow(api_key, workflow_id, messages=None):
    bp_instance = Baseprompt(api_key)
    return bp_instance.run_workflow(workflow_id, messages)
