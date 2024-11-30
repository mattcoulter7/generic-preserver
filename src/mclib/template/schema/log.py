import typing as T

from mclib.core.db.document.schema import DocumentModel

from .request import TemplateRequest
from .response import TemplateResponse


class TemplateLog(DocumentModel):
    request: TemplateRequest
    response: TemplateResponse
    metadata: T.Dict
