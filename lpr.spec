Summary:	Print server and client for local and remote printing
Summary(de):	Druckserver und Client zum Drucken im Lokal- und Fernbetrieb
Summary(fr):	Serveur d'impression et client pour l'impression \
Summary(fr):	locale ou distante.
Summary(pl):	Serwer wydruku i oprogramowanie klienckie do lokalnego i 
Summary(pl):	zdalnego drukowania.
Summary(tr):	Yerel ve uzak yazýcýlara eriþim için sunucu ve istemci
Name:		lpr
Version:	0.33
Release:	5
Copyright:	distributable
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	%{name}-%{version}.tar.gz
Source1:	lpd.init
Source2:	lpd.sysconfig
Patch0:		%{name}-misc.patch
Prereq:		/sbin/chkconfig
Buildroot:	/tmp/%{name}-%{version}-root

%description
This package manages printing services. It manages print queues, sends jobs
to local printers and remote pritners, and accepts jobs from remote clients.

%description -l de
Dieses Paket ist zuständig für Druckdienste. Es verwaltet 
Druckwarteschlangen, versendet Aufträge an lokal angeschlossene und 
entfernte Drucker und nimmt Aufträge von Remote-Clients entgegen. 

%description -l fr
Ce paquetage gère les services d'impression. Il s'occupe des files d'attente,
envoie les travaux aux imprimantes locales et distantes et reçoit les travaux
des clients distants.

%description
Pakiet zawiera oprogramowanie do zarz±dzania kolejkami wydruku,
wysy³ania zadañ drukowania do drukarek localnych i zdalnych, oraz 
przyjmowania zleceñ wydruku od zdalnych klientów.

%description -l tr
Bu paket, yazdýrma hizmetlerini, yani paket yazýcý kuyruklarýný yönetir.
Yerel ve uzak yazýcýlara iþ yollar ve uzak istemcilerden iþ kabul eder.

%prep
%setup -q
%patch -p1

%build
make OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig},var/lock}
install -d $RPM_BUILD_ROOT%{_prefix}/{bin,sbin,share/man/man{1,5,8}}
install -d $RPM_BUILD_ROOT%{_datadir}/fonts/vfont/{B,I,R,S}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lpd

make \
    DESTDIR=$RPM_BUILD_ROOT \
    install 

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man[158]/*

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

%attr(755,root,root) /etc/rc.d/init.d/lpd
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*

%attr(4710,root,lp) %{_bindir}/lpq
%attr(4710,root,lp) %{_bindir}/lpr
%attr(4710,root,lp) %{_bindir}/lprm
%attr(0755,root,lp) %{_bindir}/lptest

%attr(2710,root,lp)   %{_sbindir}/lpc
%attr(0755,root,root) %{_sbindir}/lpd
%attr(0755,root,root) %{_sbindir}/lpf
%attr(0755,root,root) %{_sbindir}/pac

%{_mandir}/man[158]/*
%{_datadir}/fonts

%ghost /var/lock/*

%changelog
* Wed Sep 30 1998 Marcin Korzonek <mkorz@shadow.eu.org>
  [0.33-4]
- translations modified for pl
- defined files permission
- allow building from non root account

* Tue Jun 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.31-5]
- build against glibc-2.1,
- major changes - follow the PLD policy.
- fixed invalid files permissions,
- start at RH spec.
