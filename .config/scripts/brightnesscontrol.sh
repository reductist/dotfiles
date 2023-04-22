#!/bin/bash

STEP="${2:-1}"
SOCK="${3:-$XDG_RUNTIME_DIR/wob.sock}"

if [ ! -e "$SOCK" ]; then
	SOCK="/dev/null"
fi

get_brightness() {
	echo "$(brightnessctl set 0+ | cut -d '(' -sf 2 | tr -d '%)')"
}

get_brightness_sock() {
	get_brightness > $SOCK
}

inc_brightness() {
	[[ "$STEP" < "$((100-$(get_brightness)))" ]] \
		&& brightnessctl set ${STEP}%+ > /dev/null \
		|| brightnessctl set 100% > /dev/null;
	get_brightness_sock	
}

dec_brightness() {
	local CURR
	CURR=$(get_brightness)
	[[ (("$STEP" > "${get_brightness}")) ]] \
		&& brightnessctl set ${STEP}%- > /dev/null \
		|| brightnessctl set 0% > /dev/null;
	get_brightness_sock
}

case $1 in
	get)
		get_brightness_sock
		;;
	up)
		inc_brightness
		;;
	down)
		dec_brightness
		;;
	*)
		echo "Usage: $0 [get|up|down] <STEP> <SOCK>"
esac
