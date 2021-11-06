from ovos_workshop import OVOSAbstractApplication
from ovos_plugin_manager.phal import find_phal_plugins, PHALPlugin
from ovos_utils.messagebus import get_mycroft_bus
from ovos_utils import  wait_for_exit_signal
from threading import Event
from time import sleep


class PHAL(OVOSAbstractApplication):
    def __init__(self, config, bus=None):
        super().__init__(skill_id="ovos.PHAL")
        self.config = config
        self.bus = bus or get_mycroft_bus()
        self.drivers = {}

    def load_plugins(self):
        for name, plug in find_phal_plugins().items():
            config = self.config.get(name) or {}
            if config.get("enabled"):
                try:
                    self.drivers[name] = plug()
                    print("PHAL plugin enabled:", name)
                except:
                    continue

    def start(self):
        self.load_plugins()
        wait_for_exit_signal()

