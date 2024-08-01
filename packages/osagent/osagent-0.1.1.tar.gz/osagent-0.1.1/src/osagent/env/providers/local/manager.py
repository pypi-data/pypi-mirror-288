import threading
import logging

from osagent.env.providers.base import VMManager

logger = logging.getLogger("desktopenv.providers.local.LocalManager")
logger.setLevel(logging.INFO)


class LocalManager(VMManager):

    def initialize_registry(self):
        pass

    def add_vm(self, vm_path, region=None):
        pass

    def occupy_vm(self, vm_path, pid, region=None):
        pass

    def delete_vm(self, vm_path, **kwargs):
        pass

    def check_and_clean(self):
        pass

    def list_free_vms(self, region):
        pass

    def get_vm_path(self, region):
        pass
