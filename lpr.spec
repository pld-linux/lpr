Summary:	Print server and client for local and remote printing
Summary(de.UTF-8):	Druckserver und Client zum Drucken im Lokal- und Fernbetrieb
Summary(fr.UTF-8):	Serveur d'impression et client pour l'impression locale ou distante
Summary(pl.UTF-8):	Serwer wydruku i oprogramowanie klienckie do lokalnego i zdalnego drukowania
Summary(tr.UTF-8):	Yerel ve uzak yazıcılara erişim için sunucu ve istemci
Name:		lpr
Version:	0.72
Release:	2.2
License:	BSD
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/lpr/%{name}-%{version}.tar.gz
# Source0-md5:	f2a46147427f20863f98b87cd9a0d772
Source1:	lpd.init
Source2:	lpd.sysconfig
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	aaa4f77e36d8778eda8f88587f7f7c4e
Patch0:		%{name}-misc.patch
Patch1:		%{name}-rmjobfix.patch
Patch2:		%{name}-getline.patch
Patch3:		%{name}-gcc.patch
Patch4:		%{name}-format.patch
Patch5:		%{name}-wait.patch
URL:		http://lpr.sourceforge.net/
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Obsoletes:	printingclient
Obsoletes:	printingdaemon
Provides:	printingclient
Provides:	printingdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package manages printing services. It manages print queues, sends
jobs to local printers and remote pritners, and accepts jobs from
remote clients.

%description -l de.UTF-8
Dieses Paket ist zuständig für Druckdienste. Es verwaltet
Druckwarteschlangen, versendet Aufträge an lokal angeschlossene und
entfernte Drucker und nimmt Aufträge von Remote-Clients entgegen.

%description -l fr.UTF-8
Ce paquetage gère les services d'impression. Il s'occupe des files
d'attente, envoie les travaux aux imprimantes locales et distantes et
reçoit les travaux des clients distants.

%description -l pl.UTF-8
Pakiet zawiera oprogramowanie do zarządzania kolejkami wydruku,
wysyłania zadań drukowania do drukarek lokalnych i zdalnych, oraz
przyjmowania zleceń wydruku od zdalnych klientów.

%description -l tr.UTF-8
Bu paket, yazdırma hizmetlerini, yani paket yazıcı kuyruklarını
yönetir. Yerel ve uzak yazıcılara iş yollar ve uzak istemcilerden iş
kabul eder.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/lock} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT%{_fontsdir}/vfont/{B,I,R,S} \
	$RPM_BUILD_ROOT/var/spool/lpd/lp

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lpd
bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

:> $RPM_BUILD_ROOT/var/lock/lpd.lock

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lpd

%preun
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del lpd
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/lpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lpd

%attr(4710,root,lp) %{_bindir}/lpq
%attr(4710,root,lp) %{_bindir}/lpr
%attr(4710,root,lp) %{_bindir}/lprm
%attr(755,root,lp) %{_bindir}/lptest

%attr(2710,root,lp) %{_sbindir}/lpc
%attr(755,root,root) %{_sbindir}/lpd
%attr(755,root,root) %{_sbindir}/lpf
%attr(755,root,root) %{_sbindir}/pac

%{_mandir}/man1/lpq.1*
%{_mandir}/man1/lpr.1*
%{_mandir}/man1/lprm.1*
%{_mandir}/man1/lptest.1*
%{_mandir}/man5/printcap.5*
%{_mandir}/man8/lpc.8*
%{_mandir}/man8/lpd.8*
%{_mandir}/man8/pac.8*
%lang(fi) %{_mandir}/fi/man[158]/*
%lang(fr) %{_mandir}/fr/man[158]/*
%lang(it) %{_mandir}/it/man[158]/*
%lang(pl) %{_mandir}/pl/man[158]/*
%{_fontsdir}/vfont

%ghost /var/lock/lpd.lock
%dir %attr(770,root,lp) %{_var}/spool/lpd
%dir %attr(770,root,lp) %{_var}/spool/lpd/lp
