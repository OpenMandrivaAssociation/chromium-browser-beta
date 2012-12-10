%define revision 147161
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
%define basever 21.0.1171.0
%define patchver() ([ -f %{_src}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_src}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-beta
Version: 21.0.1180.49
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
%{_crdir}/ui_resources_standard.pak
%{_crdir}/theme_resources_standard.pak
%{_crdir}/themes
%{_crdir}/default_apps
#%{_crdir}/xdg-mime
#%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png


%changelog
* Thu Jul 19 2012 Claudio Matsuoka <claudio@mandriva.com> 21.0.1180.49-1mdv2012.0
+ Revision: 810270
- new upstream release 21.0.1180.49 (147161)
  * Several crash fixes (Issues: 134550, 129446)
  * Fixed Autofill does not work in Incognito mode (Issue: 137100)
  * Fixed Chrome never stops blocking power save features once blocked on
    KDE (Issue: 137538)
  * Fixed Linux users experiencing slowdown due to accessibility being
    turned on (Issue: 137537)

* Mon Jul 16 2012 Claudio Matsuoka <claudio@mandriva.com> 21.0.1180.41-2
+ Revision: 809831
- new upstream release 21.0.1180.41 (146467)
  * Updated V8 - 3.11.10.14
  * Several crash fixes (Issues: 132119, 134263, 134582, 130772, 133108,
    134695, 135691, 136413, 133096)
  * Fixed horizontal scrollbar flash on uber page (Issue: 129406)
  * Fixed cloud printers not showing full list (Issue: 134242)
  * Fixed profile editing on uber page (Issue: 132343)
  * Fixed buffered area disappearing while playing video (Issues: 133567,
    131444)
  * Fixed fullscreen-mode entry and lack of video problem (Issue: 117021)

* Tue Jul 10 2012 Claudio Matsuoka <claudio@mandriva.com> 21.0.1180.15-1
+ Revision: 808797
- use system flac and speex
- new upstream release 21.0.1180.15 (144745)
- move chromium 21 from unstable to beta
- remove chromium 19
- new upstream release 19.0.1084.41 (134854)
- new upstream release 19.0.1084.36 (133841)
- new upstream release 15-19.0.1084.24 (131971)
- new upstream release 19.0.1081.2
- new upstream release 19.0.1084.15
- move chromium 19 from unstable to beta
- requires udev-devel
- new upstream release 18.0.1025.113 (127419)
- fix required package names

* Fri Jan 20 2012 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.33-1
+ Revision: 762988
- rpmlint compliance changes
- new upstream release 17.0.963.33 (117157)
  * fixes a number of stability and UI issues
- detailed changelog: http://goo.gl/Xeyp9

* Fri Jan 06 2012 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.26-1
+ Revision: 758338
- new upstream release 17.0.963.26 (116225)
  * New Extensions APIs
  * Updated Omnibox Prerendering
  * Download Scanning Protection
  * Many other small changes
- detailed changelog: http://goo.gl/Cjymx
- move chromium 17 from unstable to beta
- remove chromium 16

* Thu Dec 08 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.63-1
+ Revision: 739085
- new upstream release 16.0.912.63 (113337)
- rename libelfutils-devel requirement to elfutils-devel
- new upstream release 16.0.912.36 (112386)

* Sat Nov 12 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.36-1
+ Revision: 730267
- only include glib.h directly
- new upstream release 16.0.912.36 (109393)
- new upsteam release 16.0.912.32 (108990)
  * new toolchain
  * multi-user preferences
- new upstream release 16.0.912.21 (108057)
- remove chromium 15
- move chromium 16 from dev to beta

* Wed Oct 26 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.106-1
+ Revision: 707422
- new upstream release 15.0.874.106 (107270)
  * fixes login issues to Barrons Online and The Wall Street Journal

* Sat Oct 22 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.102-1
+ Revision: 705638
- new upstream release 15.0.874.102 (106587)
  * crash fix (75604)
  * fix to crash reporting on Linux

* Thu Oct 20 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.100-1
+ Revision: 705543
- new upstream release 15.0.874.100 (106180)
  * Updated V8 - 3.5.10.22
  * Numerous buffering fixes and optimizations for HTML5 media elements.
    (99775, 99749, 100439)
  * Tuned the omnibox to recognize more types of inputs as intranet
    navigations (99131, 94806)
  * Fixed several crashes and hangs (98975, 98948, 98955, 96861)
  * Fixed Omnibox enters keyword search mode incorrectly (95454)
  * Fixed partially visible toolbar in fullscreen mode (97177)
- detailed changelog: http://goo.gl/jI2B3

* Thu Oct 13 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.92-1
+ Revision: 704619
- new upstream release 15.0.874.92 (104978)
  * Updated V8 - 3.5.10.17
  * Fixed crash during Print Preview (96063)
  * Fixed excessive margins in printing (92000)
  * Fixed large downloads don't show progress (94468)
  * Fixed Netflix/Silverlight error (97319)
  * Disabled acceleration for background pages (96006)
  * Restored the old bookmark menus (93674)
  * Added support for an optional "requirements" section in extension/app
    manifests (99241)
- detailed changelog at http://goo.gl/snR2f
- add armv7l support
- add missing NaCl helper
- add missing XDG MIME utility script
- add extra icons
- new upstream release 15.0.874.81 (103858)
  * Updated V8 - 3.5.10.15
  * Match main window notification subscription/unsubscription in
    BookmarkBarController
  * Fixed a deadlock induced by this pref being set in response to bookmark
    sync events (97955)
  * Enable floating bookmarks bar for NTP4 for M15 beta branch (98572)
- add missing image resources from release 15.0.874.51
- detailed changelog at http://goo.gl/oapYt

* Mon Oct 03 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.54-1
+ Revision: 702536
- new upstream release 15.0.874.54 (103250)
  * Updated V8 - 3.5.10.14
  * Notification promos work with New Tab Page (Issue: 93201)
- detailed changelog at http://goo.gl/dl37M

* Wed Sep 28 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.51-1
+ Revision: 701791
- requires libelfutils-devel
- new upstream release 15.0.874.51 (102895)
  * Updated V8 - 3.5.10.13
  * Several crash fixes (including 96727, 93314, 97165, 96282)
  * Intranet URLs don't inline autocomplete (Issue 94805)
  * The New Tab Page bookmark pane has been reverted to the detached bar
    pending future improvements to the pane version (Issue: 92609)
  * Only show NTP4 info bubble for upgrading users (Issue 97103)
  * Sync not enforcing server legal bookmark names when migrating to new
    specifics (Issue 96623)
  * Native Client startup fixed for 32-bit Linux (Issue 92964)

* Thu Sep 22 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.21-1
+ Revision: 700996
- new upstream release 15.0.874.21 (101896)
  * A brand new New Tab Page
  * Javascript Fullscreen API is now enabled by default
  * Chrome Web Store items can now be installed inline by their verified site
  * Omnibox History is now an additional sync data type
- detailed changelog at http://goo.gl/7Xioy
- move chromium 15 from unstable to beta
- remove chromium 14
- new upstream release 14.0.835.186 (101896)

* Sat Sep 17 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.163-1
+ Revision: 700170
- new upstream release 14.0.835.163 (101024)
  * re-enable the enhanced completion functionality
  * additional stability patches
- detailed changelog at http://goo.gl/ELj7C

* Tue Sep 13 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.162-1
+ Revision: 699659
- new upstream release 14.0.835.162 (100637)
- detailed changelog at http://goo.gl/JAgUC

* Tue Sep 06 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.157-1
+ Revision: 698505
- new upstream release 14.0.835.157 (99685)
  * stability fixes
  * revoking trust for SSL certificates issued by DigiNotar-controlled
    intermediate CAs used by the Dutch PKIoverheid program
- detailed changelog at http://goo.gl/0FQ8C

* Fri Sep 02 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.126-1
+ Revision: 697907
- new upstream release 14.0.835.126 (99097)
  * "As part of Chrome's 3rd birthday celebration, we're happy to announce
    what you've all been waiting for: a third Beta channel release for
    this week!"
  * stability fixes
- detailed changelog at http://goo.gl/gzVY3

* Thu Sep 01 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.124-1
+ Revision: 697731
- new upstream release 14.0.835.124 (98877)
  * fixes plugin stability issues and other bugs
- detailed changelog at http://goo.gl/TlWjw

* Wed Aug 31 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.122-1
+ Revision: 697620
- new upstream release 14.0.835.122 (98753)
  * fixes a number of stability issues along with other bugs
- detailed changelog at http://goo.gl/hKpGM

* Wed Aug 17 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.94-1
+ Revision: 695071
- new upstream release 14.0.835.94 (96725)
  * fixes for a number of stability issues along with other bugs
- detailed changelog at http://goo.gl/YW2Pa

* Fri Aug 12 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.35-1
+ Revision: 694251
- remove Chromium 13
- new upstream release 14.0.835.35 (96116)
  * Initial release of Native Client
  * Web Audio API
  * Sync Encryption for all data
  * Experimental Web Request extension API
  * Experimental Content Settings extension API
- detailed changelog at http://goo.gl/CV23G (trunk) and http://goo.gl/9JgLW
- move Chromium 14 from unstable to beta
- new upstream release 13.0.782.109 (95193)
- detailed changelog at http://goo.gl/MYW78
- new upstream release 13.0.782.107 (94237)

* Thu Jul 21 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.99-1
+ Revision: 690862
- new upstream release 13.0.782.99 (93404)
- file removal moved to helper script
- detailed changelog at http://goo.gl/HO6Yl

* Thu Jun 30 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.41-1
+ Revision: 688400
- new upstream release 13.0.782.41 (91147)
- detailed changelog at http://goo.gl/7WB7a

* Thu Jun 23 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.32-1
+ Revision: 686857
- new upstream release 13.0.782.32 (90266)
- detailed changelog at http://goo.gl/I6Nqq

* Fri Jun 17 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.24-1
+ Revision: 685883
- remove Chromium 12 source files
- move Chromium 13 from unstable to beta

* Tue Jun 07 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.91-1
+ Revision: 683000
- new upstream release 12.0.742.91 (beta)
  * additional stability fixes

* Fri Jun 03 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.77-1
+ Revision: 682564
- new upstream release 12.0.742.77 (beta)
  * UI updates and performance fixes
- detailed changelog at http://goo.gl/BmPqA
- new upstream release 12.0.742.68 (beta)
  * UI updates and preformance fixes
- detailed changelog at http://goo.gl/8twhH

* Thu May 19 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.60-1
+ Revision: 676148
- new upstream release 12.0.742.60 (beta)
  * UI tweaks and performance fixes
- detailed changelog at http://goo.gl/os3dJ

* Fri May 13 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.53-1
+ Revision: 674359
- new upstream release 12.0.742.53 (beta)
  * UI tweaks and performance fixes
- detailed changelog at http://goo.gl/qkXD3

* Mon May 09 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.30-1
+ Revision: 673086
- new upstream version 12.0.742.30 (beta)
  * Hardware accelerated 3D CSS
  * New Safe Browsing protection against downloading malicious files
  * Ability to delete Flash cookies from inside Chrome
  * Launch Apps by name from the Omnibox
  * Integrated Sync into new settings pages
  * Improved screen reader support
- detailed changelog at http://goo.gl/kzSB4

* Sat May 07 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.65-1
+ Revision: 671611
- new upstream release 11.0.696.65 (beta)
  * fix issue 80580: After deleting bookmarks on the Bookmark managers,
    the bookmark bar doesn't display properly with existing bookmarks.

* Thu Apr 28 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.57-1
+ Revision: 660154
- execute gcc 4.6 preprocessor without -P option
- new upstream release 11.0.696.57 (beta)
  * fix issue 80216: left property broken with position:fixed elements in RTL
    documents
  * detailed changelog at http://goo.gl/2BU3F

* Tue Apr 19 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.50-1
+ Revision: 655873
- new upstream release 11.0.696.50 (beta)
  * fix issue 71591: Flash does not load until the tab gets activated
  * fix issue 78938: Going to settings from notification popup crashes Chrome
  * fix issue 58540: Disable speech input for readonly and disabled input
    fields
- detailed changelog at http://goo.gl/RfLvF
- new upstream release 11.0.696.48 (beta)
- fix build with gcc 4.6
- new upstream release 11.0.696.43 (beta)
  * fix issue 78548: passwords sync commits after EVERY browser restart
  * fix issue 78509: Autofill fails to fill forms
  * fix issues 78688, 68350, 77665, 74585, 76092, 77219 and 77447: A few
    known crashes
  * fix issue 60018: Redirect to my site without CFInstall.js
  * fix issue 78005: Update Silverlight v3 version metadata
  * fix issue 78120: Blocked plug-in dialog: make sure "Run this time"
    button is the first one
  * fix issue 78016: Proxy configuration over policy does not work
  * fix issue 75302: Editing style adds the word "initial" for any property
    value that uses a paren
- detailed changelog at http://goo.gl/A6U3K

* Tue Apr 05 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.34-1
+ Revision: 650436
- new upstream release 11.0.696.34 (beta)
  * Switch from using Speex to FLAC for speech input requests (Issue 61677)
  * fix issue 77653: FLACEncoder::Encode has mismatched free
  * fix issue 75862: hang on form submit with lots of stored autofill profiles
  * fix issue 76963: Browser crash if tab is closed while page is being
    downloaded

* Sun Apr 03 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.28-1
+ Revision: 649987
- new upstream release 11.0.696.28 (beta)
  * update translations

* Tue Mar 29 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.25-1
+ Revision: 648749
- new upstream release 11.0.696.25 (beta)
  * fix Issue 76991: cloud print: Error running service on headless machine
  * fix Issue 76268: sync: Not registering for NIGORI data types
  * fix Issue 76998: A known crash
  * fix Issue 74905: img of extensions not displayed in chrome://extensions
    within an incognito window
  * fix Issue 77232: Cloud policy fetch loop upon POLICY_NOT_FOUND answer
    from the server
  * fix Issue 77185: Token fetcher doesn't correctly enter unmanaged state
  * fix Issue 77421: Memory Leak in ChromeFrame in
    AutomationResourceMessageFilter::SetCookiesForUrl function
  * fix Issue 74764: Arrows not showing up on tabstrip while dropping links
  * fix Issue 76634: Java: Direct users to the right download page
  * fix Issue 62715: add es-419, fr-Foo and en-Foo and zh_HK/zh_Hant_HK to
    Accept-Language list
- detailed changelog at http://goo.gl/hp2fJ

* Wed Mar 23 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.16-1
+ Revision: 647725
- require pam development files
- new upstream version 11.0.696.16 (beta)
  * HTML5 speech input API
  * GPU-accelerated 3D CSS
  * The brand new shiny Chrome icon
- detailed changelog at http://goo.gl/43Qiq
- copy Chromium 11.0.696.12 patch from dev channel
- copy Chromium 11.0.696.16 patch from dev channel
- copy Chromium 11.0.696.14 patch from dev channel
- copy Chromium 11.0.696.3 patch from dev channel
- copy speech recording icon from dev channel
- copy Chromium 11.0.696.12 theme from dev channel
- copy Chromium 11.0.696.1 from dev channel
- copy patch from dev channel
- revert some of the system library settings introduced in revision 647138

  + Funda Wang <fwang@mandriva.org>
    - build with more system libs

* Fri Mar 18 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.151-1
+ Revision: 646283
- new upstream release 10.0.648.151 (beta)
  * blacklist a small number of HTTPS certificates

* Sat Mar 12 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.133-1
+ Revision: 644043
- new upstream release 10.0.648.133 (beta)
  * [CVE-2011-1290] fix memory corruption in style handling
- check presence of patch files
- apply patches correctly
- move chromium patch 10.0.648.114 from beta channel to stable
- move chromium patch 10.0.648.82 from beta channel to stable
- move chromium patch 10.0.648.127 from beta channel to stable
- move chromium patch 10.0.648.126 from beta channel to stable
- move chromium 10.0.648.45 from beta channel to stable
- move patch from beta channel to stable
- move patch from beta channel to stable
- new upstream release 10.0.648.127 (beta)
  * fix crash on "Disable individual plug-ins"
- detailed changelog at http://goo.gl/kUkEz
- new upstream release 10.0.648.126 (beta)
  * stability improvements and UI tweaks
  * known issue: [Bug 74709] Clicking "Disable individual plug-ins" in
    Options causes crash
- detailed changelog at http://goo.gl/a5rLr

* Thu Feb 24 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.114-3
+ Revision: 639730
+ rebuild (emptylog)

* Thu Feb 24 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.114-2
+ Revision: 639712
- update to upstream 10.0.648.114 (beta)
- package NaCl plugin

* Fri Feb 18 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.82-2
+ Revision: 638595
- new upstream 10.0.648.82 moved from unstable to beta
- move 10.0.648.82 patch from unstable to beta
- move 10.0.648.45 base tarball from unstable to beta

* Tue Feb 15 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.98-1
+ Revision: 637881
- package creation

