#!/bin/sh
# Times the screen off and puts it to background
swayidle \
    timeout  300 'hyprctl dispatch "output * dpms off"' \
    resume 'hyprctl dispatch "output * dpms on"' &
# Locks the screen immediately
swaylock
# Kills last background task so idle timer doesn't keep running
kill %%
