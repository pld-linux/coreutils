
# TODO: check patches in {sh-,file,text}utils packages

Summary:	GNU Core-utils - basic command line utilities
Summary(pl):	GNU Core-utils - podstawowe narz�dzia dzia�aj�ce z linii polece�
Name:		coreutils
Version:	4.5.3
Release:	0.8
License:	GPL
Group:		Applications/System
Source0:	ftp://alpha.gnu.org/gnu/fetish/%{name}-%{version}.tar.bz2
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/fileutils-non-english-man-pages.tar.bz2
Source2:	sh-utils-non-english-man-pages.tar.bz2
# Source3 TODO:
# - update pl (at least cksum.1,ptx.1,sort.1)
# - add es od.1(?),paste.1,pr.1 (from man-pages-es-extra)
Source3:	textutils-non-english-man-pages.tar.bz2
# to be put in Source1
Source4:	stat.1.pl
Source5:	DIR_COLORS
Source6:	fileutils.sh
Source7:	fileutils.csh
Source10:	su.pamd
Patch0:		%{name}-ac_fix.patch
Patch1:		%{name}-pam.patch
Patch2:		%{name}-info.patch
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1.7
BuildRequires:	gettext-devel
Provides:	fileutils
Provides:	sh-utils
Provides:	stat
Provides:	textutils
Obsoletes:	fileutils
Obsoletes:	sh-utils
Obsoletes:	stat
Obsoletes:	textutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Narz�dzia podstawowe (core utilities) GNU to po��czone paczki GNU
fileutils, sh-utils i textutils.

Wi�kszo�� z zawartych program�w jest znacznie ulepszona w por�wnaniu
z ich Uniksowymi odpowiednikami, np. szybciej dzia�aj�, maj� dodatkowe
opcje i mniej ogranicze�.

Programy zawarte w tej paczce to:

  basename cat chgrp chmod chown chroot cksum comm cp csplit cut date dd
  df dir dircolors dirname du echo env expand expr factor false fmt fold
  ginstall head hostid id join link ln logname ls md5sum mkdir mkfifo
  mknod mv nice nl nohup od paste pathchk pinky pr printenv printf ptx
  pwd rm rmdir seq sha1sum shred sleep sort split stat stty su sum sync
  tac tail tee test touch tr true tsort tty uname unexpand uniq unlink
  users vdir wc who whoami yes

%prep
%setup -q -a1 -a3
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gettextize}
# don't ask:
mv -f m4/inttypes.m4~ m4/inttypes.m4
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pam

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,%{_bindir},%{_sbindir},/etc/pam.d,/etc/profile.d}

%{__make} -C po install DESTDIR=$RPM_BUILD_ROOT
%{__make} -C man install DESTDIR=$RPM_BUILD_ROOT
%{__make} -C doc install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{uptime,hostname,groups}.1*

install src/{dir,dircolors,dirname,du,env,expr,factor,hostid,logname,mkfifo,\
pathchk,pinky,printenv,printf,seq,shred,stat,tee,tty,users,vdir,who,whoami,\
yes,cksum,comm,csplit,cut,expand,fmt,fold,head,join,md5sum,nohup,nl,od,paste,\
pr,ptx,sha1sum,split,sum,tac,tail,test,tr,tsort,unexpand,uniq,wc} \
	$RPM_BUILD_ROOT%{_bindir}
install src/ginstall $RPM_BUILD_ROOT%{_bindir}/install

ln -sf test $RPM_BUILD_ROOT%{_bindir}/[

install src/{basename,cat,chgrp,chmod,chown,cp,date,dd,df,echo,false,id,link,\
ln,ls,mkdir,mknod,mv,nice,pwd,rm,rmdir,sleep,sort,stty,su,sync,touch,true,\
unlink,uname} $RPM_BUILD_ROOT/bin

install src/chroot $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE6} %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/su

mv -f man/pt_BR/*.1 man/pt
for d in cs da de es fi fr hu id it ja ko nl pl pt ru ; do
	install -d $RPM_BUILD_ROOT%{_mandir}/$d/man1
	install man/$d/*.1 $RPM_BUILD_ROOT%{_mandir}/$d/man1
done
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/pl/man1/stat.1
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
rm -f $RPM_BUILD_ROOT%{_mandir}/*/man1/{groups,hostname,uptime}.1

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
%attr(755,root,root) /bin/[^s]*
%attr(755,root,root) /bin/s[^u]*
%attr(4755,root,root) /bin/su
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/su
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/DIR_COLORS
%attr(755,root,root) /etc/profile.d/*
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
%{_infodir}/coreutils.info*
