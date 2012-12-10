Summary:	Ping/Traceroute network diagnostic tool
Name:		mtr
Version:	0.82
Release:	1
Group:		Networking/Other
License:	GPLv2+
URL:		http://www.bitwizard.nl/mtr
Source0:	ftp://ftp.bitwizard.nl/mtr/%{name}-%{version}.tar.gz
Patch0:		mtr-0.71-underflow.patch
Patch1:		mtr-crash-in-xml-mode.patch
Patch2:		mtr-xml-format-fixes.patch
Patch3:		mtr-now-waits-for-last-response.patch
BuildRequires:	imagemagick
BuildRequires:  gtk2-devel
BuildRequires:	ncurses-devel
BuildRequires:	autoconf
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p0 -b .underflow
%patch1 -p1
%patch2 -p1
%patch3 -p1
touch ChangeLog

%build
autoreconf
%configure2_5x \
    --enable-gtk2

%make && mv mtr xmtr && %make distclean

# mmm, broken configure script
#export GTK_CONFIG=/dev/null 
%configure2_5x \
    --without-gtk

%make

%install
rm -rf %{buildroot}

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
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Xmtr
Comment=Ping/Traceroute network diagnostic tool
Exec=%{_bindir}/xmtr
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;System;Monitor;
EOF

%if %mdkversion < 200900
%post gtk
%update_menus
%update_desktop_database
%endif
 
%if %mdkversion < 200900
%postun gtk
%clean_menus
%clean_desktop_database
%endif

%clean
rm -rf %{buildroot}

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
%{_datadir}/applications/*.desktop


%changelog
* Mon Dec 05 2011 Alexander Khrukin <akhrukin@mandriva.org> 0.82-1
+ Revision: 737959
- version update 0.82

* Mon Nov 01 2010 Oden Eriksson <oeriksson@mandriva.com> 0.80-3mdv2011.0
+ Revision: 591434
- sync with mtr-0.80-1.fc15.src.rpm

* Sun Sep 12 2010 Oden Eriksson <oeriksson@mandriva.com> 0.80-2mdv2011.0
+ Revision: 577801
- seems to build fine without libgtk+-devel

* Tue Aug 24 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.80-1mdv2011.0
+ Revision: 572620
- update to 0.80

* Mon Oct 05 2009 Oden Eriksson <oeriksson@mandriva.com> 0.75-3mdv2010.0
+ Revision: 453966
- rediffed one fuzzy patch
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.75-1mdv2009.1
+ Revision: 298218
- 0.75
- drop redundant patches; P0,P1

* Wed Sep 03 2008 Oden Eriksson <oeriksson@mandriva.com> 0.74-1mdv2009.0
+ Revision: 279782
- 0.74

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 0.73-2mdv2009.0
+ Revision: 268172
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri May 23 2008 Frederik Himpe <fhimpe@mandriva.org> 0.73-1mdv2009.0
+ Revision: 210729
- Add BuildRequires: libgtk+-devel, otherwise %%configure fails
- New version (fixes CVE-2008-2357)
- Sync patches with Fedora

* Sun Apr 13 2008 Oden Eriksson <oeriksson@mandriva.com> 0.72-4mdv2009.0
+ Revision: 192661
- fix #40044 (mtr-gtk was build without gtk support)

* Fri Mar 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.72-3mdv2008.1
+ Revision: 187831
- fix deps (fixes #38873)
- build it against gtk2

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 02 2007 Funda Wang <fwang@mandriva.org> 0.72-2mdv2008.1
+ Revision: 114401
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - do not harcode icon extension

* Mon May 21 2007 Antoine Ginies <aginies@mandriva.com> 0.72-1mdv2008.0
+ Revision: 29466
- release 0.72

