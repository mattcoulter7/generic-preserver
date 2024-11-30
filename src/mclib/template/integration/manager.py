import logging

from mclib.core.client_abstraction.factory.config_util import get_from_config
from mclib.core.client_abstraction.factory.instantiators.abstract.shared import SharedAbstractManagerInstantiator
from mclib.core.client_abstraction.factory.instantiators.abstract.dedicated import DedicatedAbstractManagerInstantiator

from mclib.template.interface import TemplateInterface
from mclib.template.abstract_manager import TemplateAbstractManager
from mclib.template.schema import TemplateVendor
from mclib.template.callback.template import TemplateCallbackManager

logger = logging.getLogger()


class TemplateInstantiator(
    DedicatedAbstractManagerInstantiator[
        TemplateInterface,
        TemplateAbstractManager,
        TemplateVendor,
    ],
):
    client_id: str = "template"

    def instantiate(
        self,
        **config,
    ) -> TemplateInterface:
        manager = super().instantiate(**config)

        manager.callback_managers = [
            TemplateCallbackManager(),
        ]

        return manager
