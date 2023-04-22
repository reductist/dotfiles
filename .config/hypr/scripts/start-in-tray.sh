#!/bin/sh

# start waybar and programs with tray icons after pause
killall waybar && waybar &
sleep 1
killall nm-applet && nm-applet --indicator &
