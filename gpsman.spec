# This spec is based on Fedora, Debian and MIB work

Name:		gpsman
Version:	6.4.2
Release:	2
Summary:	A GPS manager
Group:		Communications
License:	GPLv3+
URL:		http://www.ncc.up.pt/gpsman/wGPSMan_4.html
Source0:	http://www.ncc.up.pt/gpsman/gpsmanhtml/gpsman-%{version}.tgz
#man files for the utils, stolen from debian
Source1:	mou2gmn.1
Source2:	mb2gmn.1
Source3:	gpsman.desktop
Source4:	gpsman-icon.png
#fix location of files in executable
Patch0:		gpsman-sourcedir.patch
BuildArch:	noarch
BuildRequires:	desktop-file-utils
Requires:	tk
Requires:	tkimg

%description
GPS Manager (GPSMan) is a graphical manager of GPS data that makes possible
the preparation, inspection and edition of GPS data in a friendly environment.

GPSMan supports communication and real-time logging with both Garmin and
Lowrance receivers and accepts real-time logging information in NMEA 0183
from any GPS receiver.

%prep
%setup -q
%patch0 -p1

#make sure all files are utf-8
recode()
{
  iconv -f "$2" -t utf-8 < "$1" > "${1}_"
  mv -f "${1}_" "$1"
}
for f in `find manual/html -name *.html`
 do recode $f iso-8859-15
done
recode manual/html/info/WPs.txt iso-8859-15

%build
#no build needed

%install
%__rm -rf %{buildroot}
#manual install
%__install -D -m 0755 gpsman.tcl %{buildroot}%{_bindir}/gpsman
%__install -Dd gmsrc %{buildroot}%{_datadir}/gpsman
for f in `find gmsrc/ -type f -maxdepth 1`
 do %__install -D -m 0644 $f %{buildroot}%{_datadir}/gpsman/`echo $f | cut -d '/' -f2`
done
%__install -Dd gmsrc/gmicons %{buildroot}%{_datadir}/gpsman/gmicons
for f in `find gmsrc/gmicons/ -type f -name *.gif`
 do %__install -D -m 0644 $f %{buildroot}%{_datadir}/gpsman/gmicons/`echo $f | cut -d '/' -f3`
done
%__install -D -m 0644 man/man1/gpsman.1 %{buildroot}%{_mandir}/man1/gpsman.1
#utils
%__install -D -m 0755 util/mb2gmn.tcl %{buildroot}%{_bindir}/mb2gmn
%__install -D -m 0755 util/mou2gmn.tcl %{buildroot}%{_bindir}/mou2gmn
#man files
%__install -D -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/mb2gmn.1
%__install -D -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/mou2gmn.1
# desktop file and icon
%__mkdir_p %{buildroot}%{_datadir}/pixmaps/
install -m 644 %{SOURCE4} \
  %{buildroot}%{_datadir}/pixmaps/
desktop-file-install --vendor="" \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE3}

%clean
%__rm -rf %{buildroot}

%files
%doc LICENSE manual/GPSMandoc.pdf manual/html
%{_bindir}/*
%{_datadir}/gpsman
%{_mandir}/man?/*
%attr(0644,root,root) %{_datadir}/applications/%{name}.desktop
%attr(0644,root,root) %{_datadir}/pixmaps/*



%changelog
* Fri Mar 02 2012 Andrey Bondrov <abondrov@mandriva.org> 6.4.2-1mdv2011.0
+ Revision: 781714
- imported package gpsman

