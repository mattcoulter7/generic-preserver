from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Self
from datetime import datetime
from abc import ABC, abstractmethod


class BaseTemplateRequest(BaseModel, ABC):
    pass

class TemplateRequest(BaseTemplateRequest):
    template_input: str
