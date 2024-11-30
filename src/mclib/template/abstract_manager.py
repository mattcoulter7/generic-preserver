import typing as T
import logging

from mclib.core.client_abstraction.manager.dedicated import DedicatedClientAbstractManager
from mclib.core.client_abstraction.manager.shared import SharedAbstractManager
from mclib.core.callback.callback_manager.base import BaseCallbackManager
from mclib.template.interface import TemplateInterface
from mclib.template.schema import (
    TemplateVendor,

    BaseTemplateRequest,
    BaseTemplateResponse,

    TemplateRequest,
    TemplateResponse,
)

logger = logging.getLogger()


class TemplateAbstractManager(
    DedicatedClientAbstractManager[
        TemplateVendor,
        TemplateInterface,
        BaseTemplateRequest,
        BaseTemplateResponse,
    ]
):
    def get_callback_event(
        self,
        response: BaseTemplateResponse
    ) -> T.Optional[str]:
        return "on_event"

    def template_func(
        self,
        request: TemplateRequest,
        *,
        metadata: T.Optional[
            T.Dict[str, T.Any]
        ] = None,
        stateless_callback_managers: T.Optional[
            T.List[BaseCallbackManager]
        ] = None,
    ) -> TemplateResponse:
        return self._perform_task(
            lambda client, request: client.template_func(request),
            request,
            metadata=metadata,
            stateless_callback_managers=stateless_callback_managers,
        )
