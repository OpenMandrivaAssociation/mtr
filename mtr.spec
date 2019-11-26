Summary:	Ping/Traceroute network diagnostic tool
Name:		mtr
Version:	0.93
Release:	1
License:	GPLv2+
Group:		Networking/Other
Url:		http://www.bitwizard.nl/mtr
Source0:	https://github.com/traviscross/mtr/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	imagemagick
BuildRequires:  autoconf
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ncurses)

%description
Mtr is a network diagnostic tool which combines Ping and Traceroute into one
program. Mtr also has two interfaces: An ncurses interface, useful for using
Mtr from a telnet session and a Gtk interface if you are using X.

%files
%doc AUTHORS COPYING FORMATS NEWS README SECURITY TODO
%attr(4755,root,ntools) %{_bindir}/mtr
%attr(4755,root,ntools) %{_sbindir}/mtr
%{_mandir}/*/*

#----------------------------------------------------------------------------

%package gtk
Summary:	Ping/Traceroute network diagnostic tool - GTK Interface
Group:		Networking/Other
Requires:	mtr

%description gtk
This is the Gtk interface for the mtr network diagnostic tool.

%files gtk
%doc AUTHORS COPYING FORMATS NEWS README SECURITY TODO
%attr(4755,root,ntools) %{_bindir}/xmtr
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/*.desktop

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
autoreconf -vfi
%configure2_5x
%make_build && mv mtr xmtr && %make_build distclean

%configure \
    --sbindir=%{_bindir} \
    --without-gtk
%make_build

%install
%make_install

for size in 16x16 32x32 48x48; do
install -d %{buildroot}%{_iconsdir}/hicolor/${size}/apps/
convert img/mtr_icon.xpm -size ${size} %{buildroot}%{_iconsdir}/hicolor/${size}/apps/%{name}.png
done

install -d %{buildroot}%{_bindir}
install -m755 xmtr %{buildroot}%{_bindir}/xmtr

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xmtr
Comment=Ping/Traceroute network diagnostic tool
Exec=xmtr
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;System;Monitor;
EOF

%files
%doc AUTHORS FORMATS NEWS README.md SECURITY TODO
%attr(-,root,ntools) %{_bindir}/mtr
%attr(-,root,ntools) %caps(cap_net_raw+ep) %{_bindir}/mtr-packet
%{_datadir}/bash-completion/completions/mtr
%{_mandir}/man8/mtr.8*
%{_mandir}/man8/mtr-packet.8*

%files gtk
%attr(-,root,ntools) %{_bindir}/xmtr
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

