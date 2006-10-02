set SYS_RC_FILE=/etc/DIR_COLORS
set USER_RC_FILE=$HOME/.dir_colors
set DEF_COLOR_MODE=tty

set COLOR_MODE=`grep ^COLOR $SYS_RC_FILE |head -n 1|cut -c 7-`

test -r $USER_RC_FILE
if ($status == 0) then
	set COLOR_MODE=`grep ^COLOR $USER_RC_FILE |head -n 1|cut -c 7-`
endif

# 'all' argument for 'ls --color=' is no longer valid
test "$COLOR_MODE" = all
if ($status == 0) then
	set COLOR_MODE=always
endif

test -z "$COLOR_MODE"
if ($status == 0) then
	set COLOR_MODE=$DEF_COLOR_MODE
endif

alias ls "ls --color=$COLOR_MODE"

test -r $USER_RC_FILE
if ($status == 0) then
	eval `/usr/bin/dircolors -c $USER_RC_FILE`
else	
	eval `/usr/bin/dircolors -c $SYS_RC_FILE`
endif

unset SYS_RC_FILE USER_RC_FILE DEF_COLOR_MODE
