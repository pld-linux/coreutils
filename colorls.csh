# skip everything for non-interactive shells
if (! $?prompt) exit

if ( "`tty -s && tput colors 2>/dev/null`" == "256" ) then
	set RC_FILE="/etc/DIR_COLORS.256color"
else
	set RC_FILE="/etc/DIR_COLORS"
endif
set USER_RC_FILE=$HOME/.dir_colors
set DEF_COLOR_MODE=auto

set COLOR_MODE=`awk '/^COLOR/{c=$2} END{print c}' $SYS_RC_FILE`

if ( -r $USER_RC_FILE ) then
	set COLOR_MODE=`awk '/^COLOR/{c=$2} END{print c}' $USER_RC_FILE`
	set RC_FILE=$USER_RC_FILE
endif

# 'all' argument for 'ls --color=' is no longer valid
if ( "$COLOR_MODE" == "all" ) then
	set COLOR_MODE=always
endif

if ( "$COLOR_MODE" == '') then
	set COLOR_MODE=$DEF_COLOR_MODE
endif

alias ls "ls --color=$COLOR_MODE"

eval `/usr/bin/dircolors -c $RC_FILE`

unset RC_FILE USER_RC_FILE DEF_COLOR_MODE COLOR_MODE
