# ovos-PHAL

ovos-PHAL is the Plugin-based Hardware Abstraction Layer for OpenVoiceOS. It runs as a service that loads PHAL plugins based on the environment, either from known configuration or from device fingerprinting. Each plugin connects a specific piece of hardware or a specific system feature to the OVOS messagebus.

A PHAL plugin can provide a hardware integration, such as a respeaker, mk1, or mk2 device. It can also provide a system integration, such as a network manager or the OVOS shell.

## Install

```bash
pip install ovos_PHAL
```

Extra plugin sets install with the package:

```bash
pip install ovos_PHAL[linux]   # alsa, system, network-manager, wallpaper-manager
pip install ovos_PHAL[mac]     # ovos-phal-plugin-mac
pip install ovos_PHAL[mk1]     # ovos-PHAL-plugin-mk1
pip install ovos_PHAL[mk2]     # ovos-PHAL-plugin-hotkeys
pip install ovos_PHAL[mk2dev]  # ovos-PHAL-plugin-mk2-fan-control
pip install ovos_PHAL[extras]  # ipgeo, connectivity-events, oauth
```

## Usage

Start the PHAL service from the command line:

```bash
ovos_PHAL
```

This reads the `PHAL` section of `mycroft.conf` and starts the plugins listed there:

```json
{
  "PHAL": {
    "ovos-PHAL-plugin-display-manager-ipc": {"enabled": true},
    "ovos-PHAL-plugin-mk1": {"enabled": true}
  }
}
```

To run PHAL from Python, use `ovos_PHAL.service.PHAL`:

```python
from ovos_PHAL.service import PHAL
from ovos_utils import wait_for_exit_signal

phal = PHAL()
phal.start()
wait_for_exit_signal()
phal.shutdown()
```

An admin variant that loads root-only plugins runs with the `ovos_PHAL_admin` command.

## Related projects

- [OpenVoiceOS/ovos-PHAL-plugin-alsa](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-alsa): ALSA audio control
- [OpenVoiceOS/ovos-PHAL-plugin-system](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-system): system-level actions (reboot, shutdown, factory reset)
- [OpenVoiceOS/ovos-PHAL-plugin-network-manager](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-network-manager): NetworkManager integration
- [OpenVoiceOS/ovos-PHAL-plugin-wallpaper-manager](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-wallpaper-manager): wallpaper management for homescreens
- [OpenVoiceOS/ovos-PHAL-plugin-oauth](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-oauth): OAuth handling over the messagebus
- [OpenVoiceOS/ovos-PHAL-plugin-connectivity-events](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-connectivity-events): connectivity change events
- [OpenVoiceOS/ovos-PHAL-plugin-ipgeo](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-ipgeo): IP-based geolocation
- [OpenVoiceOS/ovos-PHAL-plugin-mk1](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-mk1): mk1 device support
- [OpenVoiceOS/ovos-PHAL-plugin-hotkeys](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-hotkeys): key press to bus event mapping

## License

Apache-2.0
