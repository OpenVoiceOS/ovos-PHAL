from ovos_workshop import OVOSAbstractApplication
from ovos_plugin_manager.phal import find_phal_plugins, PHALPlugin
from ovos_utils.messagebus import get_mycroft_bus
from ovos_utils import wait_for_exit_signal
from ovos_utils.log import LOG
from ovos_utils.configuration import read_mycroft_config
from threading import Event
from time import sleep


class PHAL(OVOSAbstractApplication):
    def __init__(self, config=None, bus=None):
        super().__init__(skill_id="ovos.PHAL")
        if not config:
            try:
                config = read_mycroft_config()["PHAL"]
            except:
                config = {}
        self.config = config
        self.bus = bus or get_mycroft_bus()
        self.drivers = {}

    def load_plugins(self):
        for name, plug in find_phal_plugins().items():
            config = self.config.get(name) or {}
            if hasattr(plug, "validator"):
                enabled = plug.validator.validate(config)
            else:
                enabled = config.get("enabled")
            if enabled:
                try:
                    self.drivers[name] = plug()
                    LOG.info(f"PHAL plugin loaded: {name}")
                except Exception:
                    LOG.exception(f"failed to load PHAL plugin: {name}")
                    continue

    def start(self):
        self.load_plugins()
        wait_for_exit_signal()

