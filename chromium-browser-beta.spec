%define revision 108990
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define basever 16.0.904.0
%define patchver() ([ -f %{_sourcedir}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_sourcedir}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-beta
Version: 16.0.912.32
Release: %mkrel 1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
Source0: chromium-%{basever}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source1000: patch-16.0.904.0-16.0.912.0.diff.xz
Source1001: binary-16.0.904.0-16.0.912.0.tar.xz
Source1002: patch-16.0.912.0-16.0.912.4.diff.xz
Source1003: binary-16.0.912.4-16.0.912.12.tar.xz
Source1004: patch-16.0.912.4-16.0.912.12.diff.xz
Source1005: patch-16.0.912.12-16.0.912.15.diff.xz
Source1006: binary-16.0.912.12-16.0.912.15.tar.xz
Source1007: patch-16.0.912.15-16.0.912.21.diff.xz
Source1008: patch-16.0.912.21-16.0.912.32.diff.xz
Source1009: binary-16.0.912.21-16.0.912.32.tar.xz
Provides: %{crname}
Conflicts: chromium-browser-unstable
Conflicts: chromium-browser-stable
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, libexpat-devel, gperf
BuildRequires: libnspr-devel, libnss-devel, libalsa-devel
BuildRequires: libglib2-devel, libbzip2-devel, libz-devel, libpng-devel
BuildRequires: libjpeg-devel, libmesagl-devel, libmesaglu-devel
BuildRequires: libxscrnsaver-devel, libdbus-glib-devel, libcups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
BuildRequires: libxslt-devel libxml2-devel libxt-devel libpam-devel
BuildRequires: libevent-devel libflac-devel libpulseaudio-devel
BuildRequires: libelfutils-devel
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
%patchver 16.0.904.0 16.0.912.0
tar xvf %{_sourcedir}/binary-16.0.904.0-16.0.912.0.tar.xz
rm ui/resources/aura/chromium-48.png
%patchver 16.0.912.0 16.0.912.4
%patchver 16.0.912.4 16.0.912.12
tar xvf %{_sourcedir}/binary-16.0.912.4-16.0.912.12.tar.xz
%patchver 16.0.912.12 16.0.912.15
tar xvf %{_sourcedir}/binary-16.0.912.12-16.0.912.15.tar.xz
%patchver 16.0.912.15 16.0.912.21
%patchver 16.0.912.21 16.0.912.32
tar xvf %{_sourcedir}/binary-16.0.912.21-16.0.912.32.tar.xz

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/chrome_version_info_linux.cc
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
	-D use_system_sqlite=0 \
	-D use_system_libxml=1 \
	-D use_system_zlib=1 \
	-D use_system_bzip2=1 \
	-D use_system_libpng=1 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_flac=1 \
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
install -m 755 %{_sourcedir}/chromium-wrapper %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
%ifnarch armv7l
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper %{buildroot}%{_crdir}/
install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
install -m 755 out/Release/xdg-mime %{buildroot}%{_crdir}/
install -m 755 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_crdir}/default_apps/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_sourcedir}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 16 22 24 26 32 48 64 128 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
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
%{_crdir}/themes
%{_crdir}/default_apps
%{_crdir}/xdg-mime
%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png
