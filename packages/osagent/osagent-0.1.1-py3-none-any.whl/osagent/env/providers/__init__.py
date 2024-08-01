from osagent.env.providers.local.manager import LocalManager
from osagent.env.providers.local.provider import LocalProvider


def create_vm_manager_and_provider(provider_name: str, region: str):
    """
    Factory function to get the Virtual Machine Manager and Provider instances based on the provided provider name.
    """
    provider_name = provider_name.lower().strip()
    if provider_name == "local":
        return LocalManager(), LocalProvider(region)
    else:
        raise NotImplementedError(f"{provider_name} not implemented!")
