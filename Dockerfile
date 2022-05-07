FROM openvoiceos/core:dev

COPY . /tmp/ovos-phal
RUN pip3 install /tmp/ovos-phal

# TODO make it optional in ovos workshop, its a bug!
RUN pip3 install adapt-parser

USER mycroft

ENTRYPOINT ovos_PHAL