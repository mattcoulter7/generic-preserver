import typing as T
import logging

from mclib.core import client
from mclib.core.dynamic.function_utilities import supports_model_fields_as_arguments

from .schema import *
from .callback import BaseCallbackManager
from .interface import TemplateInterface

logger = logging.getLogger()


@supports_model_fields_as_arguments(
    reserved_keys=["metadata", "stateless_callback_managers", "config_override"]
)
def template_func(
    request: TemplateRequest,
    *,
    metadata: T.Optional[
        T.Dict[str, T.Any]
    ] = None,
    stateless_callback_managers: T.Optional[
        T.List[BaseCallbackManager]
    ] = None,
    config_override: T.Optional[
        dict
    ] = None,
) -> str:
    template_client: TemplateInterface = client("template", **(config_override or {}))

    response: TemplateResponse = template_client.template_func(
        request=request,
        metadata=metadata,
        stateless_callback_managers=stateless_callback_managers,
    )

    return response.template_output
