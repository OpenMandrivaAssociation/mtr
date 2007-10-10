Summary:	Ping/Traceroute network diagnostic tool
Name:		mtr
Version:	0.72
Release:	%mkrel 1
Group:		Networking/Other
License:	GPL
URL:		http://www.BitWizard.nl/mtr
Source0:	ftp://ftp.bitwizard.nl/mtr/%{name}-%{version}.tar.bz2
Patch0:		mtr-0.69-CVE-2002-0497.patch
BuildRequires:	ImageMagick
BuildRequires:	gtk-devel
#BuildRequires:	automake1.7
BuildRequires:	autoconf2.5
Buildroot:	%{_tmppath}/%{name}-buildroot

%description
Mtr is a network diagnostic tool which combines Ping and Traceroute into one
program. Mtr also has two interfaces: An ncurses interface, useful for using
Mtr from a telnet session and a Gtk interface if you are using X.

%package	gtk
Summary:	Ping/Traceroute network diagnostic tool - GTK Interface
Group:		Networking/Other
Requires:	mtr
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description	gtk
This is the Gtk interface for the mtr network diagnostic tool.

%prep

%setup -q
%patch0 -p1 -b .CVE-2002-0497

%build
export WANT_AUTOCONF_2_5=1
#rm -f configure
#rm -rf autom4te.cache
#libtoolize --copy --force && aclocal-1.7 && autoconf --force && autoheader
autoconf

%configure2_5x

%make && mv mtr xmtr && %make distclean

# mmm, broken configure script
#export GTK_CONFIG=/dev/null 
%configure2_5x \
    --without-gtk

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

cat > %{buildroot}/%{_menudir}/%{name} <<EOF
?package(xmtr-gtk): \
command="%{_bindir}/xmtr" \
icon="%{name}.png" \
title="Xmtr" \
longtitle="Ping/Traceroute network diagnostic tool" \
needs="X11" \
section="System/Monitoring" \
xdg="true"
EOF

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Xmtr
Comment="Ping/Traceroute network diagnostic tool"
Exec=%{_bindir}/xmtr
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

%post gtk
%update_menus
%update_desktop_database
 
%postun gtk
%clean_menus
%clean_desktop_database

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING FORMATS INSTALL NEWS README SECURITY TODO
%attr(4755,root,ntools) %{_bindir}/mtr
%attr(4755,root,ntools) %{_sbindir}/mtr
%{_mandir}/*/*

%files gtk
%defattr(-,root,root)
%doc AUTHORS COPYING FORMATS INSTALL NEWS README SECURITY TODO
%attr(4755,root,ntools) %{_bindir}/xmtr
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_menudir}/%{name}
%{_datadir}/applications/*.desktop


