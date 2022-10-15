#!/bin/bash

dir="/sys/class/backlight/intel_backlight/brightness"
dirmax="/sys/class/backlight/intel_backlight/max_brightness"

function get_bright {
    cat $dir
}

function get_max {
    cat $dirmax
}

function send_notification {
    br=$(get_bright)
    max=$(get_max)
    val=$(( 100 * $br / $max ))
    notify-send -u low "bright: ${val}%"
}

send_notification
