Summary:     Print server and client for local and remote printing
Summary(de): Druckserver und Client zum Drucken im Lokal- und Fernbetrieb
Summary(fr): Serveur d'impression et client pour l'impression locale ou distante
Summary(pl): Serwer wydruku i oprogramowanie klienckie do lokalnego i zdalnego drukowania
Summary(tr): Yerel ve uzak yazýcýlara eriþim için sunucu ve istemci
Name:        lpr
Version:     0.33
Release:     2
Copyright:   distributable
Group:       Utilities/System
Source:      %{name}-%{version}.tar.gz
Prereq:      /sbin/chkconfig
Buildroot:   /tmp/%{name}-%{version}-root

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

%description -l pl
Pakiet zawiera oprogramowanie do zarz±dzania kolejkami wydruków,
wysy³ania zadañ drukowania do drukarek localnych i zdalnych, oraz 
przyjmowania zleceñ wydruku od zdalnych klientów.

%description -l tr
Bu paket, yazdýrma hizmetlerini, yani paket yazýcý kuyruklarýný yönetir.
Yerel ve uzak yazýcýlara iþ yollar ve uzak istemcilerden iþ kabul eder.

%prep
%setup -q

%build
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/{usr/{bin,man/man{1,5,8},sbin},var/spool/lpd}

install lpd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd

install -s lpq/lpq lpr/lpr lprm/lprm lptest/lptest $RPM_BUILD_ROOT/usr/bin
install -s lpc/lpc lpd/lpd pac/pac filters/lpf $RPM_BUILD_ROOT/usr/sbin

install lpq/lpq.1 lpr/lpr.1 lprm/lprm.1 lptest/lptest.1 $RPM_BUILD_ROOT/usr/man/man1
install printcap.5 $RPM_BUILD_ROOT/usr/man/man5
install lpc/lpc.8 lpd/lpd.8 pac/pac.8 $RPM_BUILD_ROOT/usr/man/man8

%post
/sbin/chkconfig --add lpd

%postun
if [ $1 = 0 ]; then
   /sbin/chkconfig --del lpd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(6755, root,  lp) /usr/bin/lpq
%attr(6755, root,  lp) /usr/bin/lpr
%attr(6755, root,  lp) /usr/bin/lprm
%attr(755, root, root) /usr/bin/lptest
%attr(644, root,  man) /usr/man/*/*
%attr(755, root,   lp) /usr/sbin/lpc
%attr(700, root, root) /usr/sbin/lpd
%attr(755, root, root) /usr/sbin/lpf
%attr(700, root, root) /usr/sbin/pac
%attr(775, root, daemon) %dir /var/spool/lpd
%attr(700, root, root) %config /etc/rc.d/init.d/lpd

%changelog
* Wed Sep 30 1998 Marcin Korzonek <mkorz@shadow.eu.org>
  [0.33-2]
- added pl translation,
- defined files permission,
- allow building from non root account.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 23 1998 Erik Troan <ewt@redhat.com>
- inclued new rmjob security fix from BSD

* Sat Apr 18 1998 Erik Troan <ewt@redhat.com>
- included rmjob patches from BSD

* Fri Feb 27 1998 Otto Hammersmith <otto@redhat.com>
- increased buffer for hostname from 32 to 1024, plenty big enough now.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- changed the initscript name from lpd.init to lpd (all links, too)

* Mon Oct 27 1997 Michael Fulbright <msf@redhat.com>
- Fixed print filters to change to printer's UID so root-squashing wont bite us

* Wed Oct  8 1997 Michael Fulbright <msf@redhat.com>
- Fixed nasty error in getprent() and forked lpd's in startup() which
  caused the printcap file to be read incorrectly.
- added #include <string.h> as needed to make compile cleaner.  

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- changes for glibc 2.0.4

* Tue Apr 22 1997 Michael Fulbright <msf@redhat.com>
- moved to v. 0.17, then 0.18 (!)
- Fixed bug on Alpha/glibc when printing to a remote queue via a filter

* Fri Mar 28 1997 Michael Fulbright <msf@redhat.com>
- Moved version up to 0.16
- Added input filter support for remote queues

* Wed Mar 05 1997 Erik Troan <ewt@redhat.com>
- Incorporated filter patch into main sources
- Removed RCS logs from source tar file
- Added patched from David Mosberger to fix __ivaliduser on Alpha's
- added -Dgetline=get_line for old glibcs (this means alpha)
