#!/bin/bash

STATUS=$(bluetoothctl show | grep Powered | cut -d " " -f2)

if [[ "$STATUS" == "yes" ]]; then
    CMD="off"
else
    CMD="on"
fi

bluetoothctl power "${CMD}"