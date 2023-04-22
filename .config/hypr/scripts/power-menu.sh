#!/bin/bash

entries="Logout Suspend Reboot Shutdown"

selected=$(printf '%s\n' $entries | wofi --conf=$HOME/.config/wofi/config.power --style=$HOME/.config/wofi/style.widgets.css | awk '{print tolower($1)}')

case $selected in
  logout)
    hyprctl dispatch exec exit;;
  suspend)
    hyprctl dispatch exec systemctl suspend;;
  reboot)
    hyprctl dispatch exec systemctl reboot;;
  shutdown)
    hyprctl dispatch 'exec systemctl poweroff -i';;
esac
