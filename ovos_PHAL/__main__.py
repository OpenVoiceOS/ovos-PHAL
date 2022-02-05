from ovos_PHAL import PHAL


def main():
    # config read from mycroft.conf
    # "PHAL": {
    #     "ovos-PHAL-plugin-display-manager-ipc": {"enabled": true},
    #     "ovos-PHAL-plugin-mk1": {"enabled": True}
    # }
    phal = PHAL()
    phal.start()
    
    
if __name__ == "__main__":
    main()
