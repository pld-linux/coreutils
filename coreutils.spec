#
# Conditional build:
%bcond_with	advcopy		# progress bar in cp (orphaned patch)
%bcond_with	multicall	# Compile all the tools in a single binary
%bcond_with	tests		# unit tests running

Summary:	GNU Core-utils - basic command line utilities
Summary(pl.UTF-8):	GNU Core-utils - podstawowe narzędzia działające z linii poleceń
Name:		coreutils
Version:	8.28
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
# Source0-md5:	e7cb20d0572cc40d9f47ede6454406d1
Source1:	%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	f7c986ebc74ccb8d08ed70141063f14c
Source2:	DIR_COLORS
Source3:	DIR_COLORS.256color
Source4:	colorls.sh
Source5:	colorls.csh
Source6:	mktemp.1.pl
Source7:	%{name}.sh
Patch0:		%{name}-info.patch
Patch1:		%{name}-getgid.patch
Patch2:		%{name}-uname-cpuinfo.patch
Patch3:		%{name}-date-man.patch

Patch6:		%{name}-fmt-wchars.patch
Patch7:		%{name}-sparc64.patch
# http://translationproject.org/latest/coreutils/pl.po (pass through msgcat to generate shorter diff)
Patch8:		%{name}-pl.po-update.patch
# from http://www.beatex.org/web/advancedcopy.html, edited by shadzik
Patch9:		%{name}-advcopy.patch
Patch10:	tests.patch
URL:		http://www.gnu.org/software/coreutils/
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11.2
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-tools >= 0.19.2
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
# ensure util-linux has su included
Conflicts:	util-linux < 2.22
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

%patch6 -p1
%ifarch sparc64
%patch7 -p1
%endif
%if %{with advcopy}
# progress-bar patch, -g,--progress-bar //if in doubt, comment it out
%patch9 -p1
%endif
%patch10 -p1

%{__mv} man/pt_BR man/pt

%{__perl} -pi -e 's@GNU/Linux@PLD Linux@' m4/host-os.m4

# allow rebuilding *.gmo
%{__rm} po/stamp-po

# 8-bit-pfx test fails under C locale:
# LC_ALL=C echo -e "ça\nçb\n"|LC_ALL=C fmt -p 'ç'
# fmt: memory exhausted
%{__sed} -i -e 25,27d tests/fmt/base.pl

# /etc/resolv.conf is blocked in pld builders, try some other file
%{__sed} -i -e 's,/etc/resolv.conf,/etc/hosts,' gnulib-tests/test-read-file.c

# getgid needs to be fixed:
# getgid: missing operand
# Try `getgid --help' for more information.
%{__rm} tests/misc/help-version.sh
%{__sed} -i -e '/misc\/help-version/d' tests/local.mk

# fails on some filesystems (like XFS), where readdir returns d_type=DT_UNKNOWN
%{__rm} tests/ls/stat-free-color.sh
%{__sed} -i -e '/ls\/stat-free-color/d' tests/local.mk

# filesystem layout dependant (fails on some xfs fs)
%{__rm} tests/dd/sparse.sh
%{__sed} -i -e '/dd\/sparse/d' tests/local.mk

# mksh is too smart for those, won't let programs fail on ulimit
# would need bash here
%{__rm} tests/misc/sort-merge-fdlimit.sh
%{__sed} -i -e '/misc\/sort-merge-fdlimit/d' tests/local.mk
%{__rm} tests/split/r-chunk.sh
%{__sed} -i -e '/split\/r-chunk/d' tests/local.mk

%build
build-aux/gen-lists-of-programs.sh --autoconf > m4/cu-progs.m4
build-aux/gen-lists-of-programs.sh --automake > src/cu-progs.mk
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} -DSYSLOG_SUCCESS -DSYSLOG_FAILURE -DSYSLOG_NON_ROOT" \
	DEFAULT_POSIX2_VERSION=199209 \
	%{?with_multicall:--enable-single-binary=symlinks} \
	--disable-silent-rules \
	--enable-install-program=arch \
	--enable-no-install-program=hostname,kill,uptime

%{__make} -j1

%if %{with tests}
sed -i -e 's#COLUMNS##g' tests/envvar-check
LC_ALL=C LANG=C %{__make} -j1 tests check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/sbin,%{_bindir},%{_sbindir},/etc/shrc.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{arch,basename,cat,chgrp,chmod,chown,cp,date,dd,\
df,echo,false,id,link,ln,ls,mkdir,mknod,mktemp,mv,nice,printf,pwd,readlink,rm,rmdir,\
sleep,sort,stat,stty,sync,touch,true,unlink,uname} $RPM_BUILD_ROOT/bin

%if %{with multicall}
%{__mv} $RPM_BUILD_ROOT{%{_bindir},/bin}/coreutils
ln -s ../../bin/coreutils $RPM_BUILD_ROOT%{_bindir}
%endif

%{__mv} $RPM_BUILD_ROOT%{_bindir}/chroot $RPM_BUILD_ROOT%{_sbindir}

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE4} %{SOURCE5} %{SOURCE7} $RPM_BUILD_ROOT/etc/shrc.d

for d in cs da de es fi fr hu id it ja ko nl pl pt ru zh_CN; do
	install -d $RPM_BUILD_ROOT%{_mandir}/$d/man1
	cp -p man/$d/*.1 $RPM_BUILD_ROOT%{_mandir}/$d/man1
done
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/pl/man1/mktemp.1
# unwanted (-f left intentionally - some manuals could have no translations)
rm -f $RPM_BUILD_ROOT%{_mandir}/*/man1/{hostname,kill,su,uptime}.1
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
%attr(755,root,root) /bin/arch
%attr(755,root,root) /bin/basename
%attr(755,root,root) /bin/cat
%attr(755,root,root) /bin/chgrp
%attr(755,root,root) /bin/chmod
%attr(755,root,root) /bin/chown
%attr(755,root,root) /bin/cp
%attr(755,root,root) /bin/date
%attr(755,root,root) /bin/dd
%attr(755,root,root) /bin/df
%attr(755,root,root) /bin/echo
%attr(755,root,root) /bin/false
%attr(755,root,root) /bin/id
%attr(755,root,root) /bin/link
%attr(755,root,root) /bin/ln
%attr(755,root,root) /bin/ls
%attr(755,root,root) /bin/mkdir
%attr(755,root,root) /bin/mknod
%attr(755,root,root) /bin/mktemp
%attr(755,root,root) /bin/mv
%attr(755,root,root) /bin/nice
%attr(755,root,root) /bin/printf
%attr(755,root,root) /bin/pwd
%attr(755,root,root) /bin/readlink
%attr(755,root,root) /bin/rm
%attr(755,root,root) /bin/rmdir
%attr(755,root,root) /bin/sleep
%attr(755,root,root) /bin/sort
%attr(755,root,root) /bin/stat
%attr(755,root,root) /bin/stty
%attr(755,root,root) /bin/sync
%attr(755,root,root) /bin/touch
%attr(755,root,root) /bin/true
%attr(755,root,root) /bin/uname
%attr(755,root,root) /bin/unlink
%attr(755,root,root) %{_bindir}/[
%attr(755,root,root) %{_bindir}/b2sum
%attr(755,root,root) %{_bindir}/base32
%attr(755,root,root) %{_bindir}/base64
%attr(755,root,root) %{_bindir}/chcon
%attr(755,root,root) %{_bindir}/cksum
%attr(755,root,root) %{_bindir}/comm
%attr(755,root,root) %{_bindir}/csplit
%attr(755,root,root) %{_bindir}/cut
%attr(755,root,root) %{_bindir}/dir
%attr(755,root,root) %{_bindir}/dircolors
%attr(755,root,root) %{_bindir}/dirname
%attr(755,root,root) %{_bindir}/du
%attr(755,root,root) %{_bindir}/env
%attr(755,root,root) %{_bindir}/expand
%attr(755,root,root) %{_bindir}/expr
%attr(755,root,root) %{_bindir}/factor
%attr(755,root,root) %{_bindir}/fmt
%attr(755,root,root) %{_bindir}/fold
%attr(755,root,root) %{_bindir}/getgid
%attr(755,root,root) %{_bindir}/groups
%attr(755,root,root) %{_bindir}/head
%attr(755,root,root) %{_bindir}/hostid
%attr(755,root,root) %{_bindir}/install
%attr(755,root,root) %{_bindir}/join
%attr(755,root,root) %{_bindir}/logname
%attr(755,root,root) %{_bindir}/md5sum
%attr(755,root,root) %{_bindir}/mkfifo
%attr(755,root,root) %{_bindir}/nl
%attr(755,root,root) %{_bindir}/nohup
%attr(755,root,root) %{_bindir}/nproc
%attr(755,root,root) %{_bindir}/numfmt
%attr(755,root,root) %{_bindir}/od
%attr(755,root,root) %{_bindir}/paste
%attr(755,root,root) %{_bindir}/pathchk
%attr(755,root,root) %{_bindir}/pinky
%attr(755,root,root) %{_bindir}/pr
%attr(755,root,root) %{_bindir}/printenv
%attr(755,root,root) %{_bindir}/ptx
%attr(755,root,root) %{_bindir}/realpath
%attr(755,root,root) %{_bindir}/runcon
%attr(755,root,root) %{_bindir}/seq
%attr(755,root,root) %{_bindir}/sha1sum
%attr(755,root,root) %{_bindir}/sha224sum
%attr(755,root,root) %{_bindir}/sha256sum
%attr(755,root,root) %{_bindir}/sha384sum
%attr(755,root,root) %{_bindir}/sha512sum
%attr(755,root,root) %{_bindir}/shred
%attr(755,root,root) %{_bindir}/shuf
%attr(755,root,root) %{_bindir}/split
%attr(755,root,root) %{_bindir}/stdbuf
%attr(755,root,root) %{_bindir}/sum
%attr(755,root,root) %{_bindir}/tac
%attr(755,root,root) %{_bindir}/tail
%attr(755,root,root) %{_bindir}/tee
%attr(755,root,root) %{_bindir}/test
%attr(755,root,root) %{_bindir}/timeout
%attr(755,root,root) %{_bindir}/tr
%attr(755,root,root) %{_bindir}/truncate
%attr(755,root,root) %{_bindir}/tsort
%attr(755,root,root) %{_bindir}/tty
%attr(755,root,root) %{_bindir}/unexpand
%attr(755,root,root) %{_bindir}/uniq
%attr(755,root,root) %{_bindir}/users
%attr(755,root,root) %{_bindir}/vdir
%attr(755,root,root) %{_bindir}/wc
%attr(755,root,root) %{_bindir}/who
%attr(755,root,root) %{_bindir}/whoami
%attr(755,root,root) %{_bindir}/yes
%attr(755,root,root) %{_sbindir}/chroot
%if %{with multicall}
%attr(755,root,root) /bin/coreutils
%attr(755,root,root) %{_bindir}/coreutils
%{_mandir}/man1/coreutils.1*
%endif
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/DIR_COLORS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/DIR_COLORS.256color
%config(noreplace) /etc/shrc.d/colorls.csh
%config(noreplace) /etc/shrc.d/colorls.sh
%config(noreplace) /etc/shrc.d/%{name}.sh
%dir %{_libdir}/coreutils
%attr(755,root,root) %{_libdir}/coreutils/libstdbuf.so
%{_mandir}/man1/arch.1*
%{_mandir}/man1/b2sum.1*
%{_mandir}/man1/base32.1*
%{_mandir}/man1/base64.1*
%{_mandir}/man1/basename.1*
%{_mandir}/man1/cat.1*
%{_mandir}/man1/chcon.1*
%{_mandir}/man1/chgrp.1*
%{_mandir}/man1/chmod.1*
%{_mandir}/man1/chown.1*
%{_mandir}/man1/chroot.1*
%{_mandir}/man1/cksum.1*
%{_mandir}/man1/comm.1*
%{_mandir}/man1/cp.1*
%{_mandir}/man1/csplit.1*
%{_mandir}/man1/cut.1*
%{_mandir}/man1/date.1*
%{_mandir}/man1/dd.1*
%{_mandir}/man1/df.1*
%{_mandir}/man1/dir.1*
%{_mandir}/man1/dircolors.1*
%{_mandir}/man1/dirname.1*
%{_mandir}/man1/du.1*
%{_mandir}/man1/echo.1*
%{_mandir}/man1/env.1*
%{_mandir}/man1/expand.1*
%{_mandir}/man1/expr.1*
%{_mandir}/man1/factor.1*
%{_mandir}/man1/false.1*
%{_mandir}/man1/fmt.1*
%{_mandir}/man1/fold.1*
%{_mandir}/man1/getgid.1*
%{_mandir}/man1/groups.1*
%{_mandir}/man1/head.1*
%{_mandir}/man1/hostid.1*
%{_mandir}/man1/id.1*
%{_mandir}/man1/install.1*
%{_mandir}/man1/join.1*
%{_mandir}/man1/link.1*
%{_mandir}/man1/ln.1*
%{_mandir}/man1/logname.1*
%{_mandir}/man1/ls.1*
%{_mandir}/man1/md5sum.1*
%{_mandir}/man1/mkdir.1*
%{_mandir}/man1/mkfifo.1*
%{_mandir}/man1/mknod.1*
%{_mandir}/man1/mktemp.1*
%{_mandir}/man1/mv.1*
%{_mandir}/man1/nice.1*
%{_mandir}/man1/nl.1*
%{_mandir}/man1/nohup.1*
%{_mandir}/man1/nproc.1*
%{_mandir}/man1/numfmt.1*
%{_mandir}/man1/od.1*
%{_mandir}/man1/paste.1*
%{_mandir}/man1/pathchk.1*
%{_mandir}/man1/pinky.1*
%{_mandir}/man1/pr.1*
%{_mandir}/man1/printenv.1*
%{_mandir}/man1/printf.1*
%{_mandir}/man1/ptx.1*
%{_mandir}/man1/pwd.1*
%{_mandir}/man1/readlink.1*
%{_mandir}/man1/realpath.1*
%{_mandir}/man1/rm.1*
%{_mandir}/man1/rmdir.1*
%{_mandir}/man1/runcon.1*
%{_mandir}/man1/seq.1*
%{_mandir}/man1/sha1sum.1*
%{_mandir}/man1/sha224sum.1*
%{_mandir}/man1/sha256sum.1*
%{_mandir}/man1/sha384sum.1*
%{_mandir}/man1/sha512sum.1*
%{_mandir}/man1/shred.1*
%{_mandir}/man1/shuf.1*
%{_mandir}/man1/sleep.1*
%{_mandir}/man1/sort.1*
%{_mandir}/man1/split.1*
%{_mandir}/man1/stat.1*
%{_mandir}/man1/stdbuf.1*
%{_mandir}/man1/stty.1*
%{_mandir}/man1/sum.1*
%{_mandir}/man1/sync.1*
%{_mandir}/man1/tac.1*
%{_mandir}/man1/tail.1*
%{_mandir}/man1/tee.1*
%{_mandir}/man1/test.1*
%{_mandir}/man1/timeout.1*
%{_mandir}/man1/touch.1*
%{_mandir}/man1/tr.1*
%{_mandir}/man1/true.1*
%{_mandir}/man1/truncate.1*
%{_mandir}/man1/tsort.1*
%{_mandir}/man1/tty.1*
%{_mandir}/man1/uname.1*
%{_mandir}/man1/unexpand.1*
%{_mandir}/man1/uniq.1*
%{_mandir}/man1/unlink.1*
%{_mandir}/man1/users.1*
%{_mandir}/man1/vdir.1*
%{_mandir}/man1/wc.1*
%{_mandir}/man1/who.1*
%{_mandir}/man1/whoami.1*
%{_mandir}/man1/yes.1*
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
