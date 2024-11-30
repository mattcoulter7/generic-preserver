import typing as T
from abc import ABC

from pydantic import BaseModel

from .vendor import TemplateVendor


class BaseTemplateResponse(BaseModel, ABC):
    vendor: TemplateVendor

class TemplateResponse(BaseTemplateResponse):
    template_output: str
