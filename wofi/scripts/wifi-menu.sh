#!/bin/bash
# Menu de Wi-Fi: lista redes, conecta (pede a senha numa caixa mascarada) e liga/desliga o rádio.
. "$(dirname "$0")/lib.sh"
command -v nmcli >/dev/null || { note "Wi-Fi" "nmcli não encontrado"; exit 1; }

ICON_ON="󰖩"; ICON_OFF="󰖪"
if [ "$(nmcli radio wifi)" != "enabled" ]; then
  sel=$(printf '%s  Ligar Wi-Fi\n' "$ICON_ON" | menu "Wi-Fi" 120) || exit 0
  [ -n "$sel" ] && nmcli radio wifi on && note "Wi-Fi" "Ligado"
  exit 0
fi

nmcli device wifi rescan >/dev/null 2>&1 &
declare -A SSID_OF SEC_OF
lines=""
# IN-USE:SIGNAL:SECURITY:SSID (-t escapa ':' como '\:'; só o SSID pode ter ':' e ele é o último campo)
while IFS= read -r row; do
  inuse="${row%%:*}"; rest="${row#*:}"
  signal="${rest%%:*}"; rest="${rest#*:}"
  sec="${rest%%:*}"; ssid="${rest#*:}"; ssid="${ssid//\\:/:}"
  [ -z "$ssid" ] && continue
  [ -n "${SSID_OF[$ssid]+x}" ] && continue            # remove duplicadas (várias APs)
  if   [ "$signal" -ge 75 ]; then bars="󰤨"; elif [ "$signal" -ge 50 ]; then bars="󰤥"
  elif [ "$signal" -ge 25 ]; then bars="󰤢"; else bars="󰤟"; fi
  lock=""; [ -n "$sec" ] && lock=" 󰌾"
  mark="  "; [ "$inuse" = "*" ] && mark="✔ "
  label="$mark$bars  $ssid$lock"
  SSID_OF[$label]="$ssid"; SEC_OF[$label]="$sec"
  lines+="$label"$'\n'
done < <(nmcli -t -f IN-USE,SIGNAL,SECURITY,SSID device wifi list --rescan no | sort -t: -k2 -nr)

sel=$(printf '%s\n%s  Atualizar lista\n%s  Desligar Wi-Fi\n' "${lines%$'\n'}" "󰑐" "$ICON_OFF" | menu "Wi-Fi" 420) || exit 0
case "$sel" in
  "") exit 0 ;;
  *"Desligar Wi-Fi") nmcli radio wifi off; note "Wi-Fi" "Desligado"; exit 0 ;;
  *"Atualizar lista") exec "$0" ;;
esac

ssid="${SSID_OF[$sel]}"; sec="${SEC_OF[$sel]}"
[ -z "$ssid" ] && exit 0

if [[ "$sel" == ✔* ]]; then                           # já conectada → desconectar
  nmcli connection down id "$ssid" >/dev/null 2>&1 && note "Wi-Fi" "Desconectado de $ssid"
  exit 0
fi

if nmcli -t -f NAME connection show | grep -qxF "$ssid"; then   # rede salva: usa a senha guardada
  out=$(nmcli connection up id "$ssid" 2>&1) && { note "Wi-Fi" "Conectado a $ssid"; exit 0; }
fi

if [ -n "$sec" ]; then
  pass=$(printf '' | menu "Senha de $ssid" 100 --password) || exit 0
  [ -z "$pass" ] && exit 0
  out=$(printf '%s\n' "$pass" | nmcli --ask device wifi connect "$ssid" 2>&1)
else
  out=$(nmcli device wifi connect "$ssid" 2>&1)
fi
if [ $? -eq 0 ]; then note "Wi-Fi" "Conectado a $ssid"
else nmcli connection delete id "$ssid" >/dev/null 2>&1; note "Wi-Fi" "Falha ao conectar a $ssid (senha incorreta?)"; fi
