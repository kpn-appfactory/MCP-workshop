FROM python:3.13.1-slim-bookworm

COPY image-content /
RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    mkdir /data && \
    useradd -m -s /bin/bash workshop && \
    chown -R workshop:workshop /scripts /configmap /data && \
    chmod 755 /scripts/workshop.py

USER workshop

CMD [ "python", "-u", "/scripts/workshop.py" ]
