Summary:	Print server and client for local and remote printing
Summary(de):	Druckserver und Client zum Drucken im Lokal- und Fernbetrieb
Summary(fr):	Serveur d'impression et client pour l'impression locale ou distante
Summary(pl):	Serwer wydruku i oprogramowanie klienckie do lokalnego i zdalnego drukowania
Summary(tr):	Yerel ve uzak yazýcýlara eriþim için sunucu ve istemci
Name:		lpr
Version:	0.33
Release:	5
Copyright:	distributable
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	%{name}-%{version}.tar.gz
Source1:	lpd.init
Source2:	lpd.sysconfig
Patch0:		%{name}-misc.patch
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package manages printing services. It manages print queues, sends
jobs to local printers and remote pritners, and accepts jobs from
remote clients.

%description -l de
Dieses Paket ist zuständig für Druckdienste. Es verwaltet
Druckwarteschlangen, versendet Aufträge an lokal angeschlossene und
entfernte Drucker und nimmt Aufträge von Remote-Clients entgegen.

%description -l fr
Ce paquetage gère les services d'impression. Il s'occupe des files
d'attente, envoie les travaux aux imprimantes locales et distantes et
reçoit les travaux des clients distants.

%description -l pl
Pakiet zawiera oprogramowanie do zarz±dzania kolejkami wydruku,
wysy³ania zadañ drukowania do drukarek localnych i zdalnych, oraz
przyjmowania zleceñ wydruku od zdalnych klientów.

%description -l tr
Bu paket, yazdýrma hizmetlerini, yani paket yazýcý kuyruklarýný
yönetir. Yerel ve uzak yazýcýlara iþ yollar ve uzak istemcilerden iþ
kabul eder.

%prep
%setup -q
%patch -p1

%build
%{__make} OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig},var/lock}
install -d $RPM_BUILD_ROOT%{_prefix}/{bin,sbin,share/man/man{1,5,8}}
install -d $RPM_BUILD_ROOT%{_datadir}/fonts/vfont/{B,I,R,S}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lpd

%{__make} install DESTDIR=$RPM_BUILD_ROOT

:> $RPM_BUILD_ROOT/var/lock/lpd.lock

%clean
rm -rf $RPM_BUILD_ROOT

%post
NAME=lpd; %chkconfig_add

%preun
NAME=lpd; %chkconfig_del

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/lpd
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
