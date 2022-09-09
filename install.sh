#!/bin/bash

INSTALL_PATH="/opt/instalker"

if [ "$UID" != 0 ]; then
    echo "[!] Run as root"
    exit 1
fi

mkdir -p $INSTALL_PATH
cp instalker.service /etc/systemd/system -vv
systemctl daemon-reload
systemctl start instalker
