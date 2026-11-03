#!/bin/bash
# Teclas Fn: volume, mudo, microfone e brilho, com aviso (barra de progresso no dunst).
# Uso: osd.sh volume up|down|mute | mic mute | brightness up|down
tag() { notify-send -a Snoopy -t 1200 -h string:x-dunst-stack-tag:osd "$@"; }
case "$1:$2" in
  volume:up)   wpctl set-mute @DEFAULT_AUDIO_SINK@ 0; wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ 5%+ ;;
  volume:down) wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%- ;;
  volume:mute) wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle ;;
  mic:mute)    wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle
               if wpctl get-volume @DEFAULT_AUDIO_SOURCE@ | grep -q MUTED; then tag "󰍭  Microfone mudo"; else tag "󰍬  Microfone ligado"; fi
               exit 0 ;;
  brightness:up)   brightnessctl -q set 5%+ ;;
  brightness:down) brightnessctl -q set 5%- ;;
  *) exit 1 ;;
esac
case "$1" in
  volume)
    out=$(wpctl get-volume @DEFAULT_AUDIO_SINK@); v=$(awk '{printf "%d", $2*100}' <<<"$out")
    if grep -q MUTED <<<"$out"; then tag "󰝟  Mudo" -h int:value:0; else tag "󰕾  Volume $v%" -h int:value:"$v"; fi ;;
  brightness)
    cur=$(brightnessctl get); max=$(brightnessctl max); p=$((cur * 100 / max))
    tag "󰃠  Brilho $p%" -h int:value:"$p" ;;
esac
