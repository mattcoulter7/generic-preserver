from mclib.core.client_abstraction.factory.instantiators.base import ClientInstantiator
from mclib.core.client_abstraction.factory.config_util import get_from_config

from mclib.template.interface import TemplateInterface
from mclib.template.vendor.vendor_1 import Vendor1TemplateClient


class Vendor1TemplateInstantiator(
    ClientInstantiator[TemplateInterface],
):
    client_id: str = "template.vendor_1"

    def instantiate(
        self,
        **config,
    ) -> TemplateInterface:
        return Vendor1TemplateClient(
            template_config_key=get_from_config(
                "TEMPLATE_CONFIG_KEY", config
            ),
        )
