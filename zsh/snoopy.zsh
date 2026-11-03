# Snoopy no terminal: cores do powerlevel10k, aliases bonitos e plugins opcionais.
# Carregado pelo ~/.zshrc, DEPOIS do ~/.p10k.zsh.

# Tema atual (Day/Night) = o include da 1ª linha do kitty.conf
_snoopy_theme=${SNOOPY_THEME:-${$(grep -om1 'snoopy-[a-z]*' ~/.config/kitty/kitty.conf 2>/dev/null):-snoopy-night}}
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

# ---- Design do prompt: segmentos arredondados em duas linhas ----
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(os_icon dir vcs newline prompt_char)
typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status command_execution_time background_jobs virtualenv nvm time)
typeset -g POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR=$'\uE0B4'
typeset -g POWERLEVEL9K_LEFT_SUBSEGMENT_SEPARATOR=$'\uE0B5'
typeset -g POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR=$'\uE0B6'
typeset -g POWERLEVEL9K_RIGHT_SUBSEGMENT_SEPARATOR=$'\uE0B7'
typeset -g POWERLEVEL9K_LEFT_PROMPT_FIRST_SEGMENT_START_SYMBOL=$'\uE0B6'
typeset -g POWERLEVEL9K_LEFT_PROMPT_LAST_SEGMENT_END_SYMBOL=$'\uE0B4'
typeset -g POWERLEVEL9K_RIGHT_PROMPT_FIRST_SEGMENT_START_SYMBOL=$'\uE0B6'
typeset -g POWERLEVEL9K_RIGHT_PROMPT_LAST_SEGMENT_END_SYMBOL=$'\uE0B4'
typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_PREFIX="%F{$SNOOPY[grey1]}╭─"
typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_PREFIX="%F{$SNOOPY[grey1]}├─"
typeset -g POWERLEVEL9K_MULTILINE_LAST_PROMPT_PREFIX="%F{$SNOOPY[grey1]}╰─"
typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_GAP_CHAR='─'
typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_GAP_FOREGROUND=$SNOOPY[bg5]
typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_GAP_FOREGROUND=$SNOOPY[bg5]
typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=true
typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_SUFFIX=
typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_SUFFIX=
typeset -g POWERLEVEL9K_MULTILINE_LAST_PROMPT_SUFFIX=
typeset -g POWERLEVEL9K_OS_ICON_CONTENT_EXPANSION=$'\uF1B0'     # patinha
typeset -g POWERLEVEL9K_PROMPT_CHAR_{OK,ERROR}_VIINS_CONTENT_EXPANSION='❯'
typeset -g POWERLEVEL9K_PROMPT_CHAR_LEFT_PROMPT_FIRST_SEGMENT_START_SYMBOL=
typeset -g POWERLEVEL9K_PROMPT_CHAR_LEFT_PROMPT_LAST_SEGMENT_END_SYMBOL=
typeset -g POWERLEVEL9K_STATUS_OK=false
typeset -g POWERLEVEL9K_STATUS_OK_PIPE=false
typeset -g POWERLEVEL9K_COMMAND_EXECUTION_TIME_THRESHOLD=2
typeset -g POWERLEVEL9K_COMMAND_EXECUTION_TIME_PRECISION=0
typeset -g POWERLEVEL9K_TIME_FORMAT='%D{%H:%M}'
typeset -g POWERLEVEL9K_TIME_BACKGROUND=$SNOOPY[bg3]
typeset -g POWERLEVEL9K_TIME_FOREGROUND=$SNOOPY[fg]
typeset -g POWERLEVEL9K_NVM_BACKGROUND=$SNOOPY[bg2]
typeset -g POWERLEVEL9K_NVM_FOREGROUND=$SNOOPY[green]
typeset -g POWERLEVEL9K_BACKGROUND_JOBS_BACKGROUND=$SNOOPY[bg2]
typeset -g POWERLEVEL9K_BACKGROUND_JOBS_FOREGROUND=$SNOOPY[blue]
typeset -g POWERLEVEL9K_VIRTUALENV_BACKGROUND=$SNOOPY[bg2]
typeset -g POWERLEVEL9K_VIRTUALENV_FOREGROUND=$SNOOPY[yellow]
typeset -g POWERLEVEL9K_TRANSIENT_PROMPT=always
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
