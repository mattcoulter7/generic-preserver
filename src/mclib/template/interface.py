import logging
import concurrent.futures
import typing as T

from abc import ABC

from mclib.template.schema import (
    TemplateRequest,
    TemplateResponse,
    TemplateVendor,
)

logger = logging.getLogger()


class TemplateInterface(ABC):
    vendor: T.Optional[TemplateVendor] = None

    def template_func(
        self,
        request: TemplateRequest,  # abstract language codes
    ) -> TemplateResponse:
        ...
