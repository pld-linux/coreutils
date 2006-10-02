SYS_RC_FILE=/etc/DIR_COLORS
USER_RC_FILE=$HOME/.dir_colors
DEF_COLOR_MODE=tty

COLOR_MODE=`grep ^COLOR $SYS_RC_FILE |head -n 1|cut -c 7-`

[ -r $USER_RC_FILE ] && COLOR_MODE=`grep ^COLOR $USER_RC_FILE |head -n 1|cut -c 7-`

# 'all' argument for 'ls --color=' is no longer valid
[ "$COLOR_MODE" = all ] && COLOR_MODE=always

[ -z "$COLOR_MODE" ] && COLOR_MODE=$DEF_COLOR_MODE

alias ls="ls --color=$COLOR_MODE"

if [ -r $USER_RC_FILE ]; then
	eval `/usr/bin/dircolors -b $USER_RC_FILE`
else	
	eval `/usr/bin/dircolors -b $SYS_RC_FILE`
fi

unset SYS_RC_FILE USER_RC_FILE DEF_COLOR_MODE COLOR_MODE
