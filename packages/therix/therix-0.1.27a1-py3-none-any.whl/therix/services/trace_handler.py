from langfuse.callback import CallbackHandler
from therix.core.version import get_current_version
import json



def get_trace_handler(trace_details=None, trace_api=None, system_prompt=None, pipeline_id=None, session_id=None,metadata=None):
    therix_trace_handler = None
    if trace_details:
        therix_trace_handler = CallbackHandler(
            secret_key=trace_details['secret_key'],
            public_key=trace_details['public_key'],
            host=trace_details["host"],
            trace_name=str(pipeline_id),
            session_id=str(session_id),
            version=get_current_version(),
            metadata=metadata
        )
    elif trace_api:
        release = json.dumps({
            "prompt_name": system_prompt.get("prompt_name"),
            "prompt_version": system_prompt.get("prompt_version")
        }) if system_prompt and system_prompt.get("prompt_name") and system_prompt.get("prompt_version") else None
        
        therix_trace_handler = CallbackHandler(
            secret_key=trace_api['secret_key'],
            public_key=trace_api['public_key'],
            host=trace_api['host'],
            trace_name=pipeline_id,
            session_id=session_id,
            version=get_current_version(),
            release=f"""{release}""",
            metadata=metadata
        )
        
    return therix_trace_handler