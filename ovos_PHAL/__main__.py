from ovos_PHAL import PHAL


if __name__ == "__main__":
    # config read from mycroft.conf
    # "PHAL": {
    #     "ovos-PHAL-plugin-display-manager-ipc": {"enabled": true},
    #     "ovos-PHAL-plugin-mk1": {"enabled": True}
    # }
    phal = PHAL()
    phal.start()
