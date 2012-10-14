#
# Conditional build:
%bcond_with	advcopy	# progress bar in cp (orphaned patch)
%bcond_without	tests	# do not perform "make test check"
#
Summary:	GNU Core-utils - basic command line utilities
Summary(pl.UTF-8):	GNU Core-utils - podstawowe narzędzia działające z linii poleceń
Name:		coreutils
Version:	8.19
Release:	0.1
License:	GPL v3+
Group:		Applications/System
Source0:	http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
# Source0-md5:	1a01231a2f3ed37c0efc073ccdda9375
Source1:	%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	f7c986ebc74ccb8d08ed70141063f14c
Source2:	DIR_COLORS
Source3:	fileutils.sh
Source4:	fileutils.csh
Source5:	mktemp.1.pl
Patch0:		%{name}-info.patch
Patch1:		%{name}-getgid.patch
Patch2:		%{name}-uname-cpuinfo.patch
Patch3:		%{name}-date-man.patch
Patch4:		%{name}-mem.patch
Patch5:		%{name}-7.4-sttytcsadrain.patch
Patch6:		%{name}-fmt-wchars.patch
Patch7:		%{name}-sparc64.patch
# http://translationproject.org/latest/coreutils/pl.po (pass through msgcat to generate shorter diff)
Patch8:		%{name}-pl.po-update.patch
# from http://www.beatex.org/web/advancedcopy.html, edited by shadzik
Patch9:		%{name}-advcopy.patch
# TODO: check/move to su in util-linux
#Source7:	runuser.pamd
#Source8:	runuser-l.pamd
#Patch1:	%{name}-pam.patch
#Patch10:	%{name}-runuser.patch
#Patch11:	%{name}-split-pam.patch
URL:		http://www.gnu.org/software/coreutils/
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-devel >= 0.18.1
BuildRequires:	gmp-devel
BuildRequires:	help2man
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel
BuildRequires:	rpmbuild(find_lang) >= 1.24
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo >= 4.2
BuildRequires:	xz
%if %{with tests}
BuildRequires:	strace
%endif
Requires:	setup >= 2.4.6-2
Provides:	fileutils
Provides:	mktemp = %{version}-%{release}
Provides:	sh-utils
Provides:	stat
Provides:	textutils
Obsoletes:	fileutils
Obsoletes:	mktemp
Obsoletes:	sh-utils
Obsoletes:	stat
Obsoletes:	textutils
Conflicts:	shadow < 1:4.0.3-6
Conflicts:	tetex < 1:2.0.2
Conflicts:	util-linux < 2.13-0.pre7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
These are the GNU core utilities. This package is the union of the GNU
fileutils, sh-utils, and textutils packages.

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer
arbitrary limits.

The programs that can be built with this package are:

  [ basename cat chgrp chmod chown chroot cksum comm cp csplit cut date
  dd df dir dircolors dirname du echo env expand expr factor false fmt
  fold install groups head hostid id join link ln logname ls md5sum
  mkdir mkfifo mknod mv nice nl nohup od paste pathchk pinky pr printenv
  printf ptx pwd realpath rm rmdir seq sha1sum shred sleep sort split
  stat stty sum sync tac tail tee test touch tr true tsort tty uname
  unexpand uniq unlink users vdir wc who whoami yes

%description -l pl.UTF-8
Narzędzia podstawowe (core utilities) GNU to połączone paczki GNU
fileutils, sh-utils i textutils.

Większość z zawartych programów jest znacznie ulepszona w porównaniu
z ich uniksowymi odpowiednikami, np. szybciej działają, mają dodatkowe
opcje i mniej ograniczeń.

Programy zawarte w tym pakiecie to:

  [ basename cat chgrp chmod chown chroot cksum comm cp csplit cut date
  dd df dir dircolors dirname du echo env expand expr factor false fmt
  fold ginstall groups head hostid id join link ln logname ls md5sum
  mkdir mkfifo mknod mv nice nl nohup od paste pathchk pinky pr printenv
  printf ptx pwd realpath rm rmdir seq sha1sum shred sleep sort split
  stat stty sum sync tac tail tee test touch tr true tsort tty uname
  unexpand uniq unlink users vdir wc who whoami yes

%prep
%setup -q -a1
%patch8 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%ifarch sparc64
%patch7 -p1
%endif
%if %{with advcopy}
# progress-bar patch, -g,--progress-bar //if in doubt, comment it out
%patch9 -p1
%endif

%{__perl} -pi -e 's@GNU/Linux@PLD Linux@' m4/host-os.m4

# allow rebuilding *.gmo
%{__rm} po/stamp-po

# fails under C locale:
# LC_ALL=C echo -e "ça\nçb\n"|LC_ALL=C fmt -p 'ç'
# fmt: memory exhausted
%{__sed} -i -e 25,27d tests/fmt/base

# /etc/resolv.conf is blocked in pld builders, try some other file
%{__sed} -i -e 's,/etc/resolv.conf,/etc/hosts,' gnulib-tests/test-read-file.c

# getgid needs to be fixed:
# getgid: missing operand
# Try `getgid --help' for more information.
%{__rm} tests/misc/help-version
%{__sed} -i -e '/misc\/help-version/d' tests/Makefile.am

# fails on some filesystems (like XFS), where readdir returns d_type=DT_UNKNOWN
%{__rm} tests/ls/stat-free-color
%{__sed} -i -e '/ls\/stat-free-color/d' tests/Makefile.am

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} -DSYSLOG_SUCCESS -DSYSLOG_FAILURE -DSYSLOG_NON_ROOT" \
	DEFAULT_POSIX2_VERSION=199209 \
	--disable-silent-rules \
	--enable-install-program=arch \
	--enable-no-install-program=hostname,kill,uptime

%{__make}

%if %{with tests}
sed -i -e 's#COLUMNS##g' tests/envvar-check
%{__make} -j1 tests check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/sbin,%{_bindir},%{_sbindir},/etc/shrc.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_bindir}/{arch,basename,cat,chgrp,chmod,chown,cp,date,dd,\
df,echo,false,id,link,ln,ls,mkdir,mknod,mktemp,mv,nice,printf,pwd,rm,rmdir,\
sleep,sort,stat,stty,sync,touch,true,unlink,uname} $RPM_BUILD_ROOT/bin

mv -f $RPM_BUILD_ROOT%{_bindir}/chroot $RPM_BUILD_ROOT%{_sbindir}

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/shrc.d

cp -a man/pt_BR man/pt
for d in cs da de es fi fr hu id it ja ko nl pl pt ru zh_CN; do
	install -d $RPM_BUILD_ROOT%{_mandir}/$d/man1
	cp -p man/$d/*.1 $RPM_BUILD_ROOT%{_mandir}/$d/man1
done
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/pl/man1/mktemp.1
# unwanted (-f left intentionally - some manuals could have no translations)
rm -f $RPM_BUILD_ROOT%{_mandir}/*/man1/{hostname,kill,uptime}.1
# always remove, never packaged but sometimes installed
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS THANKS-to-translators TODO
%attr(755,root,root) /bin/[!s]*
%attr(755,root,root) /bin/s[!u]*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/chroot
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/DIR_COLORS
%config(noreplace) /etc/shrc.d/fileutils.*sh
%dir %{_libdir}/coreutils
%attr(755,root,root) %{_libdir}/coreutils/libstdbuf.so
%{_mandir}/man1/*
%lang(cs) %{_mandir}/cs/man1/*
%lang(da) %{_mandir}/da/man1/*
%lang(de) %{_mandir}/de/man1/*
%lang(es) %{_mandir}/es/man1/*
%lang(fi) %{_mandir}/fi/man1/*
%lang(fr) %{_mandir}/fr/man1/*
%lang(hu) %{_mandir}/hu/man1/*
%lang(id) %{_mandir}/id/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(ko) %{_mandir}/ko/man1/*
%lang(nl) %{_mandir}/nl/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(pt) %{_mandir}/pt/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%lang(zh_CN) %{_mandir}/zh_CN/man1/*
%{_infodir}/coreutils.info*
