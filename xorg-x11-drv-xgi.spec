%define tarball xf86-video-xgi
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
#define gitdate 20121114

%if 0%{?gitdate}
%define gver .%{gitdate}git
%endif

Summary:   Xorg X11 xgi video driver
Name:      xorg-x11-drv-xgi
Version:   1.6.1
Release:   1%{?gver}%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

%if 0%{?gitdate}
Source0:   %{tarball}-%{gitdate}.tar.bz2
%else
Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif
Source1:   xgi.xinf

Patch1: xgi-1.6.0-ulong.patch
Patch4: xgi-1.6.0-module-data.patch
Patch6: xgi-1.6.0-xorg-version-current.patch
Patch7: xgi-z9s-fix-dpms.patch
Patch8: xgi-1.6.1-open.patch

ExcludeArch: s390 s390x

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-devel >= 1.13.0
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1

Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 xgi video driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{?!gitdate:%{version}}
%patch1 -p1 -b .ulong
%patch4 -p1 -b .module-data
%patch6 -p1 -b .xvc
%patch7 -p1 -b .dpms
%patch8 -p1 -b .open

%build
%if 0%{?gitdate}
autoreconf -v --install || exit 1
%endif
%configure --disable-static --disable-xaa
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{moduledir}
%dir %{driverdir}
%{driverdir}/xgi_drv.so
%{_datadir}/hwdata/videoaliases/xgi.xinf
#%dir %{_mandir}/man4x
%{_mandir}/man4/xgi.4*

%changelog
* Wed Nov 11 2015 Adam Jackson <ajax@redhat.com> 1.6.1-1
- xgi 1.6.1

* Wed Nov 11 2015 Adam Jackson <ajax@redhat.com> - 1.6.0-21.20121114git
- Rebuild for server 1.17

* Thu Sep 11 2014 Adam Jackson <ajax@redhat.com> 1.6.0-20
- Fix initialization to work post-mibs-removal

* Wed Apr 23 2014 Adam Jackson <ajax@redhat.com> 1.6.0-19
- Sync with git and rebuild for server 1.15

* Fri Jan 18 2013 Adam Jackson <ajax@redhat.com> 1.6.0-18
- Silence amazing amounts of log spam in the i2c code (#888607)
- Fix a crash in DDC fetch (#888607)

* Mon Jan 07 2013 Adam Jackson <ajax@redhat.com> 1.6.0-17
- Fix crash in mode validation (#873599)
- Explicitly build without XAA

* Wed Nov 14 2012 Adam Jackson <ajax@redhat.com> 1.6.0-16
- Sync with git (#873599)

* Tue Aug 29 2012 Jerome Glisse <jglisse@redhat.com> 1.6.0-14.20120807git
- Resolves: #835267

* Wed Aug 22 2012 airlied@redhat.com - 1.6.0-13.20120807git
- rebuild for server ABI requires

* Tue Aug 07 2012 Jerome Glisse <jglisse@redhat.com> 1.6.0-12-20120807
- temporary git snapshot, to fix deps after X server rebuild

* Tue Sep 13 2011 Adam Jackson <ajax@redhat.com> 1.6.0-11
- spec fix (#708157)

* Fri Aug 05 2011 Adam Jackson <ajax@redhat.com> 1.6.0-10
- xgi-z9s-fix-dpms.patch: Fix DPMS-on on XG21 chips, including Z9s and
  Z9m (#704094)

* Tue Jun 28 2011 Ben Skeggs <bskeggs@redhat.com> - 1.6.0-8
- rebuild for 6.2 server rebase

* Tue Apr 26 2011 Adam Jackson <ajax@redhat.com> 1.6.0-7
- xgi-1.6.0-xorg-version-current.patch: Yet more yet more API skew. (#631738)

* Mon Apr 25 2011 Adam Jackson <ajax@redhat.com> 1.6.0-6
- xgi-1.6.0-symlists.patch: Yet more API skew. (#631738)

* Tue Apr 05 2011 Adam Jackson <ajax@redhat.com>
- xgi-1.6.0-module-data.patch: Export loader hook. (#693652)

* Mon Mar 28 2011 Adam Jackson <ajax@redhat.com> 1.6.0-4
- s@MIT/X11@MIT@ in License tag.

* Thu Mar 17 2011 Adam Jackson <ajax@redhat.com> 1.6.0-3
- Initial RHEL build. (#631738)
