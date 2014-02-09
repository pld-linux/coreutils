# Skip all for noninteractive shells.
[ -z "$PS1" ] && return

if [ "`tty -s && tput colors 2>/dev/null`" = "256" ]; then
	RC_FILE="/etc/DIR_COLORS.256color"
else
	RC_FILE="/etc/DIR_COLORS"
fi
USER_RC_FILE=$HOME/.dir_colors
DEF_COLOR_MODE=auto

COLOR_MODE=`awk '/^COLOR/{c=$2} END{print c}' $RC_FILE`

if [ -r $USER_RC_FILE ]; then
	COLOR_MODE=`awk '/^COLOR/{c=$2} END{print c}' $USER_RC_FILE`
	RC_FILE=$USER_RC_FILE
fi

# 'all' argument for 'ls --color=' is no longer valid
[ "$COLOR_MODE" = all ] && COLOR_MODE=always

[ -z "$COLOR_MODE" ] && COLOR_MODE=$DEF_COLOR_MODE

alias ls="ls --color=$COLOR_MODE"

eval `/usr/bin/dircolors -b $RC_FILE`

unset RC_FILE USER_RC_FILE DEF_COLOR_MODE COLOR_MODE
