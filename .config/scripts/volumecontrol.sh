#!/bin/bash

STEP="${2:-5}"
SOCK="${3:-/dev/null}"

is_muted_sink() {
    pactl get-sink-mute @DEFAULT_SINK@ | cut -c 7-9 | tr -d ' '
}

is_muted_source() {
    pactl get-source-mute @DEFAULT_SOURCE@ | cut -c 7-9 | tr -d ' '
}

get_volume_sink() {
    pactl get-sink-volume @DEFAULT_SINK@ | grep '%' | cut -d '/' -f 2 | tr -d ' %'
}

get_volume_source() {
    pactl get-source-volume @DEFAULT_SOURCE@ | grep '%' | cut -d '/' -f 2 | tr -d ' %'
}

wob_volume_sink() {
    get_volume_sink > "$SOCK"
}

wob_volume_source() {
    get_volume_source > "$SOCK"
}

incr_volume() {
    local CURR
    CURR=$(get_volume_sink)
    local MAX=$((100-CURR))
    if (("$STEP" >= "$MAX")); then
        pactl set-sink-volume @DEFAULT_SINK@ 100%
    else
        pactl set-sink-volume @DEFAULT_SINK@ "+${STEP}%"
    fi
    wob_volume_sink
}

decr_volume() {
    local CURR
    CURR=$(get_volume_sink)
    if (("$STEP" > "$CURR")); then
        STEP="$CURR"
    fi
    pactl set-sink-volume @DEFAULT_SINK@ "-${STEP}%"
    wob_volume_sink
}

mute_source() {
    pactl set-source-mute @DEFAULT_SOURCE@ toggle
    if [[ "$(is_muted_source)" == "no" ]]; then
        echo 0 > "$SOCK"
    else
        wob_volume_source
    fi
}

mute_sink() {
    pactl set-sink-mute @DEFAULT_SINK@ toggle
    if [[ "$(is_muted_sink)" == "no" ]]; then
        wob_volume_sink
    else
        echo 0 > "$SOCK"
    fi
}

mute_both() {
    mute_source;
    mute_sink;
}

case $1 in
    up)
        incr_volume
        ;;
    down)
        decr_volume
        ;;
    mute_source)
        mute_source    
        ;;
    mute_sink)
        mute_sink
        ;;
    mute_both)
        mute_both
        ;;
esac