Summary:	Coreutils
Summary(pl):	Coreutils
Name:		coreutils
Version:	4.5.1
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.bz2
#BuildRequires:	
#Requires:	
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
# when no spec requires sh/file/text utils Provides can be removed
Provides:	sh-utils
Provides:	fileutils
Provides:	textutils

%define	_prefix	/usr

%description
These are the GNU core utilities.  This package is the union of
the GNU fileutils, sh-utils, and textutils packages.

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer
arbitrary limits.

The programs that can be built with this package are:

  basename cat chgrp chmod chown chroot cksum comm cp csplit cut date dd
  df dir dircolors dirname du echo env expand expr factor false fmt fold
  ginstall groups head hostid hostname id join kill link ln logname ls
  md5sum mkdir mkfifo mknod mv nice nl nohup od paste pathchk pinky pr
  printenv printf ptx pwd rm rmdir seq sha1sum shred sleep sort split
  stat stty su sum sync tac tail tee test touch tr true tsort tty uname
  unexpand uniq unlink uptime users vdir wc who whoami yes

%description -l pl
Narzêdzia rdzeniowe (core utilities) GNU to po³±czone paczki GNU fileutils,
sh-utils i textutils.

Wiêkszo¶æ z zawartych programów jest znacznie ulepszona w porównaniu
z ich Uniksowymi odpowiednikami, np. szybciej dzia³aj±, maj± dodatkowe
opcje i mniej ograniczeñ.

Programy zawarte w tej paczce to:

  basename cat chgrp chmod chown chroot cksum comm cp csplit cut date dd
  df dir dircolors dirname du echo env expand expr factor false fmt fold
  ginstall groups head hostid hostname id join kill link ln logname ls
  md5sum mkdir mkfifo mknod mv nice nl nohup od paste pathchk pinky pr
  printenv printf ptx pwd rm rmdir seq sha1sum shred sleep sort split
  stat stty su sum sync tac tail tee test touch tr true tsort tty uname
  unexpand uniq unlink uptime users vdir wc who whoami yes

%prep
%setup -q

#%patch

%build
./configure --prefix=%{_prefix}
%{__make} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir},%{_infodir},%{_mandir}/man1,/bin,/sbin}
#%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} install

#%find_lang 

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
