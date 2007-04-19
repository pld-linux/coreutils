#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
#
Summary:	GNU Core-utils - basic command line utilities
Summary(pl.UTF-8):	GNU Core-utils - podstawowe narzędzia działające z linii poleceń
Name:		coreutils
Version:	6.9
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.bz2
# Source0-md5:	c9607d8495f16e98906e7ed2d9751a06
Source1:	%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	f7c986ebc74ccb8d08ed70141063f14c
Source2:	DIR_COLORS
Source3:	fileutils.sh
Source4:	fileutils.csh
Source5:	su.pamd
Source6:	su-l.pamd
Source7:	runuser.pamd
Source8:	runuser-l.pamd
Patch0:		%{name}-info.patch
Patch1:		%{name}-pam.patch
Patch2:		%{name}-getgid.patch
Patch3:		%{name}-su-paths.patch
Patch4:		%{name}-uname-cpuinfo.patch
Patch5:		%{name}-date-man.patch
Patch6:		%{name}-mem.patch
Patch7:		%{name}-install-C.patch
Patch8:		%{name}-po.patch
Patch9:		%{name}-no-nb.patch
Patch10:	%{name}-fmt-wchars.patch
Patch11:	%{name}-runuser.patch
Patch12:	%{name}-split-pam.patch
Patch13:	%{name}-selinux.patch
Patch14:	%{name}-pl.po-update.patch
URL:		http://www.gnu.org/software/coreutils/
BuildRequires:	acl-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9.6
%{?with_selinux:BuildRequires:	gcc >= 5:3.2}
BuildRequires:	gettext-devel >= 0.16-2
BuildRequires:	help2man
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	pam-devel
BuildRequires:	texinfo >= 4.2
Requires:	pam >= 0.77.3
Requires:	setup >= 2.4.6-2
Provides:	fileutils
Provides:	sh-utils
Provides:	stat
Provides:	textutils
Obsoletes:	fileutils
Obsoletes:	sh-utils
Obsoletes:	stat
Obsoletes:	textutils
Conflicts:	shadow < 1:4.0.3-6
Conflicts:	tetex < 1:2.0.2
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
  printf ptx pwd rm rmdir seq sha1sum shred sleep sort split stat stty
  su sum sync tac tail tee test touch tr true tsort tty uname unexpand
  uniq unlink users vdir wc who whoami yes

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
  printf ptx pwd rm rmdir seq sha1sum shred sleep sort split stat stty
  su sum sync tac tail tee test touch tr true tsort tty uname unexpand
  uniq unlink users vdir wc who whoami yes

%prep
%setup -q -a1
%patch14 -p1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%{?with_selinux:%patch13 -p1}

%{__perl} -pi -e 's@GNU/Linux@PLD Linux@' m4/host-os.m4

# no_NO is just an alias for nb_NO in recent glibc
# no.po is outdated, nb.po is more fresh here (see also patch10)
rm -f po/no.*
# allow rebuilding *.gmo
rm -f po/stamp-po

# missing, added to gettext.m4 by ./bootstrap
echo 'AC_DEFUN([gl_LOCK_EARLY],[])' > m4/gllock.m4

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} -DSYSLOG_SUCCESS -DSYSLOG_FAILURE -DSYSLOG_NON_ROOT" \
	DEFAULT_POSIX2_VERSION=199209 \
	%{?with_selinux:--enable-selinux} \
	--enable-pam

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/sbin,%{_bindir},%{_sbindir},/etc/pam.d,/etc/shrc.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_bindir}/{hostname,kill,uptime}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{hostname,kill,uptime}.1*

mv -f $RPM_BUILD_ROOT%{_bindir}/{basename,cat,chgrp,chmod,chown,cp,date,dd,df,\
echo,false,id,link,ln,ls,mkdir,mknod,mv,nice,printf,pwd,rm,rmdir,sleep,sort,stty,\
sync,touch,true,unlink,uname} $RPM_BUILD_ROOT/bin

mv -f $RPM_BUILD_ROOT%{_bindir}/chroot $RPM_BUILD_ROOT%{_sbindir}

# su is missed by "make install"
install src/su $RPM_BUILD_ROOT/bin
install src/runuser $RPM_BUILD_ROOT/sbin

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/shrc.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/su
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/su-l
install %{SOURCE7} $RPM_BUILD_ROOT/etc/pam.d/runuser
install %{SOURCE8} $RPM_BUILD_ROOT/etc/pam.d/runuser-l

cp -a man/pt_BR man/pt
for d in cs da de es fi fr hu id it ja ko nl pl pt ru zh_CN ; do
	install -d $RPM_BUILD_ROOT%{_mandir}/$d/man1
	install man/$d/*.1 $RPM_BUILD_ROOT%{_mandir}/$d/man1
done
rm -f $RPM_BUILD_ROOT%{_mandir}/*/man1/{hostname,kill,uptime}.1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS THANKS-to-translators TODO
%attr(755,root,root) /bin/[!s]*
%attr(755,root,root) /bin/s[!u]*
%attr(4755,root,root) /bin/su
%attr(755,root,root) /sbin/runuser
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/su
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/su-l
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/runuser
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/runuser-l
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/DIR_COLORS
/etc/shrc.d/*
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
