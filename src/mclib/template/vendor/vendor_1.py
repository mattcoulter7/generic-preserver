import typing as T
import logging

from mclib.template.schema import (
    TemplateRequest,
    TemplateResponse,
    TemplateVendor,
)
from mclib.template.interface import TemplateInterface

logger = logging.getLogger()


class Vendor1TemplateClient(TemplateInterface):
    vendor: T.Optional[TemplateVendor] = TemplateVendor.VENDOR_1

    def __init__(
        self,
        template_config_key: str,
    ) -> None:
        self.template_config_key = template_config_key

    def template_func(
        self,
        request: TemplateRequest,
    ) -> TemplateResponse:
        return TemplateResponse(
            vendor=self.vendor,
            template_output=request.template_input,
        )
