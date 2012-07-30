%define revision 148591
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
%define basever 21.0.1171.0
%define patchver() ([ -f %{_src}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_src}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-beta
Version: 21.0.1180.57
Release: %mkrel 1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
Source0: chromium-%{basever}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source1000: patch-21.0.1171.0-21.0.1180.0.diff.xz
Source1001: binary-21.0.1171.0-21.0.1180.0.tar.xz
Source1002: script-21.0.1171.0-21.0.1180.0.sh
Source1003: patch-21.0.1180.0-21.0.1180.4.diff.xz
Source1004: binary-21.0.1180.0-21.0.1180.4.tar.xz
Source1005: script-21.0.1180.0-21.0.1180.4.sh
Source1006: patch-21.0.1180.4-21.0.1180.11.diff.xz
Source1007: binary-21.0.1180.4-21.0.1180.11.tar.xz
Source1008: script-21.0.1180.4-21.0.1180.11.sh
Source1009: patch-21.0.1180.11-21.0.1180.15.diff.xz
Source1010: binary-21.0.1180.11-21.0.1180.15.tar.xz
Source1011: script-21.0.1180.11-21.0.1180.15.sh
Source1012: patch-21.0.1180.15-21.0.1180.41.diff.xz
Source1013: binary-21.0.1180.15-21.0.1180.41.tar.xz
Source1014: script-21.0.1180.15-21.0.1180.41.sh
Source1015: patch-21.0.1180.41-21.0.1180.49.diff.xz
Source1016: patch-21.0.1180.49-21.0.1180.57.diff.xz
Source1017: binary-21.0.1180.49-21.0.1180.57.tar.xz
Source1018: script-21.0.1180.49-21.0.1180.57.sh
Patch0: chromium-21.0.1171.0-remove-inline.patch
Provides: %{crname}
Conflicts: chromium-browser-unstable
Conflicts: chromium-browser-stable
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, expat-devel, gperf
BuildRequires: nspr-devel, nss-devel, libalsa-devel
BuildRequires: glib2-devel, bzip2-devel, zlib-devel, libpng-devel
BuildRequires: jpeg-devel, mesagl-devel, mesaglu-devel
BuildRequires: libxscrnsaver-devel, dbus-glib-devel, cups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
BuildRequires: libxslt-devel libxml2-devel libxt-devel pam-devel
BuildRequires: libevent-devel libflac-devel pulseaudio-devel
BuildRequires: elfutils-devel udev-devel speex-devel yasm
BuildRequires: pkgconfig(libusb-1.0)
ExclusiveArch: i586 x86_64 armv7l

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the beta channel Chromium browser. From time to time stable and
complete features are moved from the unstable browser to beta. It's a
middle ground between the stable and unstable browsers, and may lack the
polish one expects from a finished product.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.

%prep
%setup -q -n chromium-%{basever}
%patch0 -p1 -b .remove-inline
%patchver 21.0.1171.0 21.0.1180.0
tar xvf %{_src}/binary-21.0.1171.0-21.0.1180.0.tar.xz
sh -x %{_src}/script-21.0.1171.0-21.0.1180.0.sh
%patchver 21.0.1180.0 21.0.1180.4
tar xvf %{_src}/binary-21.0.1180.0-21.0.1180.4.tar.xz
sh -x %{_src}/script-21.0.1180.0-21.0.1180.4.sh
%patchver 21.0.1180.4 21.0.1180.11
tar xvf %{_src}/binary-21.0.1180.4-21.0.1180.11.tar.xz
sh -x %{_src}/script-21.0.1180.4-21.0.1180.11.sh
%patchver 21.0.1180.11 21.0.1180.15
sh -x %{_src}/script-21.0.1180.11-21.0.1180.15.sh
%patchver 21.0.1180.15 21.0.1180.41
tar xvf %{_src}/binary-21.0.1180.15-21.0.1180.41.tar.xz
sh -x %{_src}/script-21.0.1180.15-21.0.1180.41.sh
%patchver 21.0.1180.41 21.0.1180.49
%patchver 21.0.1180.49 21.0.1180.57
tar xvf %{_src}/binary-21.0.1180.49-21.0.1180.57.tar.xz
sh -x %{_src}/script-21.0.1180.49-21.0.1180.57.sh

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_crdir}/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_crdir}/chrome \
	-D linux_link_gnome_keyring=0 \
	-D use_gconf=0 \
	-D werror='' \
	-D use_system_v8=0 \
	-D use_system_sqlite=0 \
	-D use_system_libxml=1 \
	-D use_system_zlib=1 \
	-D use_system_bzip2=1 \
	-D use_system_xdg_utils=1 \
	-D use_system_yasm=1 \
	-D use_system_libusb=1 \
	-D use_system_libpng=1 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_flac=1 \
	-D use_system_speex=1 \
	-D use_system_vpx=0 \
	-D use_system_icu=0 \
%ifarch i586
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i586"
%endif
%ifarch armv7l
	-D target_arch=arm \
	-D disable_nacl=1 \
	-D linux_use_tcmalloc=0 \
	-D armv7=1 \
	-D release_extra_cflags="-marm"
%endif

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_crdir}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_src}/chromium-wrapper %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/ui_resources_standard.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/theme_resources_standard.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
%ifnarch armv7l
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper %{buildroot}%{_crdir}/
install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
#install -m 755 out/Release/xdg-mime %{buildroot}%{_crdir}/
#install -m 755 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_crdir}/default_apps/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# Strip NaCl IRT
./native_client/toolchain/linux_x86_newlib/bin/x86_64-nacl-strip --strip-debug %{buildroot}%{_crdir}/nacl_irt_x86_64.nexe
./native_client/toolchain/linux_x86_newlib/bin/i686-nacl-strip --strip-debug %{buildroot}%{_crdir}/nacl_irt_x86_32.nexe

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_src}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 22 24 48 64 128 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{crname}.png
done
for i in 16 26 32; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{crname}.png
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{crname}
%{_crdir}/chromium-wrapper
%{_crdir}/chrome
%{_crdir}/chrome-sandbox
%{_crdir}/chrome.pak
%{_crdir}/libffmpegsumo.so
%ifnarch armv7l
%{_crdir}/libppGoogleNaClPluginChrome.so
%{_crdir}/nacl_helper_bootstrap
%{_crdir}/nacl_helper
%{_crdir}/nacl_irt_*.nexe
%endif
%{_crdir}/locales
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/ui_resources_standard.pak
%{_crdir}/theme_resources_standard.pak
%{_crdir}/themes
%{_crdir}/default_apps
#%{_crdir}/xdg-mime
#%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png
