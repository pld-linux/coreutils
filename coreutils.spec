
# TODO: check patches in {sh-,file,text}utils packages
# e.g. su in coreutils doesn't have PAM support!!!

Summary:	Coreutils
Summary(pl):	Coreutils
Name:		coreutils
Version:	4.5.3
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	ftp://alpha.gnu.org/gnu/fetish/%{name}-%{version}.tar.bz2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
# when no spec requires sh/file/text utils Provides can be removed
Provides:	fileutils
Provides:	sh-utils
Provides:	textutils
Obsoletes:	fileutils
Obsoletes:	sh-utils
Obsoletes:	stat
Obsoletes:	textutils

%description
These are the GNU core utilities.  This package is the union of
the GNU fileutils, sh-utils, and textutils packages.

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer
arbitrary limits.

The programs that can be built with this package are:

  basename cat chgrp chmod chown chroot cksum comm cp csplit cut date dd
  df dir dircolors dirname du echo env expand expr factor false fmt fold
  ginstall head hostid id join link ln logname ls md5sum mkdir mkfifo
  mknod mv nice nl nohup od paste pathchk pinky pr printenv printf ptx
  pwd rm rmdir seq sha1sum shred sleep sort split stat stty su sum sync
  tac tail tee test touch tr true tsort tty uname unexpand uniq unlink
  users vdir wc who whoami yes

%description -l pl
Narzêdzia podstawowe (core utilities) GNU to po³±czone paczki GNU
fileutils, sh-utils i textutils.

Wiêkszo¶æ z zawartych programów jest znacznie ulepszona w porównaniu
z ich Uniksowymi odpowiednikami, np. szybciej dzia³aj±, maj± dodatkowe
opcje i mniej ograniczeñ.

Programy zawarte w tej paczce to:

  basename cat chgrp chmod chown chroot cksum comm cp csplit cut date dd
  df dir dircolors dirname du echo env expand expr factor false fmt fold
  ginstall head hostid id join link ln logname ls md5sum mkdir mkfifo
  mknod mv nice nl nohup od paste pathchk pinky pr printenv printf ptx
  pwd rm rmdir seq sha1sum shred sleep sort split stat stty su sum sync
  tac tail tee test touch tr true tsort tty uname unexpand uniq unlink
  users vdir wc who whoami yes

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C po install DESTDIR=$RPM_BUILD_ROOT
%{__make} -C man install DESTDIR=$RPM_BUILD_ROOT mandir="%{_mandir}"
%{__make} -C doc install DESTDIR=$RPM_BUILD_ROOT prefix="%{_datadir}"

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir},%{_infodir},%{_mandir}/man1,/bin}

install src/{dir,dircolors,dirname,du,env,expr,factor,hostid,logname,mkfifo,pathchk,pinky,printenv,printf,seq,shred,stat,tee,tty,users,vdir,who,whoami,yes,\
cksum,comm,csplit,cut,expand,fmt,fold,head,join,md5sum,nl,od,paste,pr,ptx,sha1sum,split,sum,tac,tail,tr,tsort,unexpand,uniq,wc} $RPM_BUILD_ROOT%{_bindir}
install src/nohup $RPM_BUILD_ROOT%{_bindir}

install src/{basename,cat,chgrp,chmod,chown,cp,date,dd,df,echo,false,id,link,ln,ls,mkdir,mknod,mv,nice,pwd,rm,rmdir,sleep,sort,stty,su,sync,test,touch,true,unlink,uname} $RPM_BUILD_ROOT/bin

install src/chroot $RPM_BUILD_ROOT%{_sbindir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc
%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%{_infodir}/*
