from ovos_PHAL import PHAL

config = {
    'ovos_phal_ipc2bus': {"enabled": True}
}
phal = PHAL(config)
phal.start()
