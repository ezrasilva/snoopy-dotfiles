# Snoopy no terminal: cores do powerlevel10k, aliases bonitos e plugins opcionais.
# Carregado pelo ~/.zshrc, DEPOIS do ~/.p10k.zsh.

# Tema atual (Day/Night) = o include da 1ª linha do kitty.conf
_snoopy_theme=${$(grep -om1 'snoopy-[a-z]*' ~/.config/kitty/kitty.conf 2>/dev/null):-snoopy-night}
source ~/.config/zsh/colors-${_snoopy_theme}.zsh 2>/dev/null || return 0

# ---- powerlevel10k (hex: o kitty tem truecolor) ----
# O ~/.p10k.zsh define 'verbose' (aviso gigante se algo imprimir no início); aqui vem depois, então vale 'quiet'.
typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet
typeset -g POWERLEVEL9K_OS_ICON_BACKGROUND=$SNOOPY[red]
typeset -g POWERLEVEL9K_OS_ICON_FOREGROUND=$SNOOPY[bg0]
typeset -g POWERLEVEL9K_DIR_BACKGROUND=$SNOOPY[blue]
typeset -g POWERLEVEL9K_DIR_FOREGROUND=$SNOOPY[bg0]
typeset -g POWERLEVEL9K_DIR_SHORTENED_FOREGROUND=$SNOOPY[bg0]
typeset -g POWERLEVEL9K_DIR_ANCHOR_FOREGROUND=$SNOOPY[bg0]
typeset -g POWERLEVEL9K_VCS_FOREGROUND=$SNOOPY[bg0]
typeset -g POWERLEVEL9K_VCS_CLEAN_BACKGROUND=$SNOOPY[green]
typeset -g POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND=$SNOOPY[green]
typeset -g POWERLEVEL9K_VCS_MODIFIED_BACKGROUND=$SNOOPY[yellow]
typeset -g POWERLEVEL9K_VCS_CONFLICTED_BACKGROUND=$SNOOPY[orange]
typeset -g POWERLEVEL9K_VCS_LOADING_BACKGROUND=$SNOOPY[grey0]
typeset -g POWERLEVEL9K_STATUS_OK_BACKGROUND=$SNOOPY[bg2]
typeset -g POWERLEVEL9K_STATUS_OK_FOREGROUND=$SNOOPY[green]
typeset -g POWERLEVEL9K_STATUS_OK_PIPE_BACKGROUND=$SNOOPY[bg2]
typeset -g POWERLEVEL9K_STATUS_ERROR_BACKGROUND=$SNOOPY[red]
typeset -g POWERLEVEL9K_STATUS_ERROR_FOREGROUND=$SNOOPY[bg0]
typeset -g POWERLEVEL9K_STATUS_ERROR_SIGNAL_BACKGROUND=$SNOOPY[red]
typeset -g POWERLEVEL9K_STATUS_ERROR_PIPE_BACKGROUND=$SNOOPY[red]
typeset -g POWERLEVEL9K_COMMAND_EXECUTION_TIME_BACKGROUND=$SNOOPY[yellow]
typeset -g POWERLEVEL9K_COMMAND_EXECUTION_TIME_FOREGROUND=$SNOOPY[fg]
typeset -g POWERLEVEL9K_PROMPT_CHAR_OK_{VIINS,VICMD,VIVIS,VIOWR}_FOREGROUND=$SNOOPY[green]
typeset -g POWERLEVEL9K_PROMPT_CHAR_ERROR_{VIINS,VICMD,VIVIS,VIOWR}_FOREGROUND=$SNOOPY[red]
(( $+functions[p10k] )) && p10k reload 2>/dev/null

# ---- aliases ----
if (( $+commands[eza] )); then
  alias ls='eza --icons --group-directories-first'
  alias ll='eza -l --icons --group-directories-first --git'
  alias la='eza -la --icons --group-directories-first --git'
  alias tree='eza --tree --icons --level=3'
fi
(( $+commands[fastfetch] )) && alias ff='fastfetch --config ~/.config/fastfetch/snoopy.jsonc'

# ---- plugins opcionais (só carregam se instalados) ----
for p in /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh; do
  [[ -f $p ]] && { source $p; ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$SNOOPY[grey1]"; }
done
[[ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && {
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  typeset -A ZSH_HIGHLIGHT_STYLES
  ZSH_HIGHLIGHT_STYLES[command]="fg=$SNOOPY[green],bold"
  ZSH_HIGHLIGHT_STYLES[builtin]="fg=$SNOOPY[green],bold"
  ZSH_HIGHLIGHT_STYLES[alias]="fg=$SNOOPY[green],bold"
  ZSH_HIGHLIGHT_STYLES[unknown-token]="fg=$SNOOPY[red]"
  ZSH_HIGHLIGHT_STYLES[path]="fg=$SNOOPY[blue],underline"
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]="fg=$SNOOPY[yellow]"
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]="fg=$SNOOPY[yellow]"
  ZSH_HIGHLIGHT_STYLES[comment]="fg=$SNOOPY[grey1]"
}
unset p _snoopy_theme
