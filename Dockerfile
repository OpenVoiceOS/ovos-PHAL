FROM ghcr.io/openvoiceos/core:dev

COPY . /tmp/ovos-phal
RUN pip3 install /tmp/ovos-phal

USER mycroft

ENTRYPOINT ovos_PHAL