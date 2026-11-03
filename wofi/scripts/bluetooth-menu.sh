#!/bin/bash
# Menu de Bluetooth: liga/desliga, procura, pareia, conecta e desconecta dispositivos.
. "$(dirname "$0")/lib.sh"
command -v bluetoothctl >/dev/null || { note "Bluetooth" "bluetoothctl não encontrado"; exit 1; }

powered() { bluetoothctl show | grep -q "Powered: yes"; }
if ! powered; then
  sel=$(printf '󰂯  Ligar Bluetooth\n' | menu "Bluetooth" 120) || exit 0
  [ -n "$sel" ] && { rfkill unblock bluetooth 2>/dev/null; bluetoothctl power on >/dev/null && note "Bluetooth" "Ligado"; }
  exit 0
fi

declare -A MAC_OF STATE_OF
lines=""
while read -r _ mac name; do
  [ -z "$mac" ] && continue
  info=$(bluetoothctl info "$mac")
  conn=no; pair=no
  grep -q "Connected: yes" <<<"$info" && conn=yes
  grep -q "Paired: yes" <<<"$info" && pair=yes
  if   [ $conn = yes ]; then icon="✔ 󰂱"; st=connected
  elif [ $pair = yes ]; then icon="  󰂯"; st=paired
  else icon="  󰂲"; st=new; fi
  label="$icon  $name"
  MAC_OF[$label]="$mac"; STATE_OF[$label]="$st"
  lines+="$label"$'\n'
done < <(bluetoothctl devices)

sel=$(printf '%s\n󰑐  Procurar dispositivos\n󰂲  Desligar Bluetooth\n' "${lines%$'\n'}" | sed '/^$/d' | menu "Bluetooth" 420) || exit 0
case "$sel" in
  "") exit 0 ;;
  *"Desligar Bluetooth") bluetoothctl power off >/dev/null; note "Bluetooth" "Desligado"; exit 0 ;;
  *"Procurar dispositivos")
      note "Bluetooth" "Procurando por 8 segundos…"
      bluetoothctl --timeout 8 scan on >/dev/null 2>&1
      exec "$0" ;;
esac

mac="${MAC_OF[$sel]}"; st="${STATE_OF[$sel]}"; name="${sel#*  }"; name="${name#*  }"
[ -z "$mac" ] && exit 0
case "$st" in
  connected) bluetoothctl disconnect "$mac" >/dev/null && note "Bluetooth" "Desconectado de $name" ;;
  paired)    if timeout 15 bluetoothctl connect "$mac" >/dev/null 2>&1; then note "Bluetooth" "Conectado a $name"
             else note "Bluetooth" "Falha ao conectar a $name"; fi ;;
  new)       note "Bluetooth" "Pareando com $name…"
             if timeout 30 bluetoothctl pair "$mac" >/dev/null 2>&1; then
               bluetoothctl trust "$mac" >/dev/null 2>&1
               timeout 15 bluetoothctl connect "$mac" >/dev/null 2>&1 && note "Bluetooth" "Conectado a $name" \
                 || note "Bluetooth" "Pareado, mas não conectou"
             else note "Bluetooth" "Falha ao parear com $name (coloque-o em modo de pareamento)"; fi ;;
esac
