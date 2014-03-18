Summary:	Ping/Traceroute network diagnostic tool
Name:		mtr
Version:	0.85
Release:	1
License:	GPLv2+
Group:		Networking/Other
Url:		http://www.bitwizard.nl/mtr
Source0:	ftp://ftp.bitwizard.nl/mtr/%{name}-%{version}.tar.gz
Patch0:		mtr-0.71-underflow.patch
Patch1:		mtr-xml-format-fixes.patch
Patch2:		mtr-crash-in-xml-mode.patch
Patch3:		mtr-now-waits-for-last-response.patch
BuildRequires:	imagemagick
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
%patch0 -p0 -b .underflow
%patch1 -p1
%patch2 -p1
%patch3 -p1
touch ChangeLog

%build
autoreconf -fi
%configure2_5x \
	--enable-gtk2

%make && mv mtr xmtr && make clean

# mmm, broken configure script
#export GTK_CONFIG=/dev/null 
%configure2_5x \
	--without-gtk

%make

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}
install -d %{buildroot}%{_menudir}

%makeinstall_std

# convert the icon
convert img/mtr_icon.xpm -size 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert img/mtr_icon.xpm -size 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert img/mtr_icon.xpm -size 48x48 %{buildroot}%{_liconsdir}/%{name}.png

install -m755 xmtr %{buildroot}%{_bindir}/

ln -s ../sbin/mtr %{buildroot}%{_bindir}/mtr

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xmtr
Comment=Ping/Traceroute network diagnostic tool
Exec=%{_bindir}/xmtr
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;System;Monitor;
EOF

