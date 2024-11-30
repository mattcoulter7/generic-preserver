import logging
import typing as T

from mclib.core.callback.callback_manager.base import BaseCallbackManager
from mclib.template.schema import (
    TemplateRequest,
    TemplateResponse,
)

logger = logging.getLogger()


class TemplateCallbackManager(BaseCallbackManager[T.Any, T.Any]):
    def on_event(
        self,
        request: TemplateRequest,
        response: TemplateResponse,
        *,
        metadata: T.Optional[T.Dict[str, T.Any]] = None,
    ) -> None:
        ...
