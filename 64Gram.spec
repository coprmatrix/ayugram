%bcond_with qt5


%{!?_metainfodir:%define _metainfodir %{_datadir}/metainfo}

#define _use_internal_dependency_generator 0
#{lua:
#rpm.define('__find_requires_basic '..rpm.expand('__find_requires'))
#rpm.define('__find_requires %{_builddir}/%{buildsubdir}/script.sh')
#}

#%define __find_requires %{SOURCE1}
# Telegram Desktop's constants...
%global appname 64Gram

# Reducing debuginfo verbosity...
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

%if 0%{?fedora} < 40 && 0%{?suse_version} < 1500
%global with_qt5 1
%endif

Name: 64Gram
Version: 1
Release: 1%{?dist}

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * cld3  - Apache-2.0 -- static dependency;
# * libprisma - MIT -- static dependency;
# * tgcalls - LGPL-3.0-only -- static dependency;
# * plasma-wayland-protocols - LGPL-2.1-or-later -- static dependency;
# * wayland-protocols - MIT -- static dependency;
License:  GPL-3.0-or-later AND Apache-2.0 AND LGPL-3.0-only AND LGPL-2.1-or-later AND MIT
URL:      https://github.com/TDesktop-x64/tdesktop

#global commit_1 aa5f6297460e1c33d844c42bc2cccd3f7428b57
#global commit_2 d61403889f94b472398e016bbe9d60f2563ce88e
%global commit_1 rawhide
%global commit_2 stable
%global pgr https://pagure.io/mochaa-rpms/64gram/raw/%{commit_1}/f/64Gram
%global cmt https://raw.githubusercontent.com/AOSC-Dev/aosc-os-abbs/%{commit_2}/app-web/telegram-desktop/autobuild/patches/

Summary:  Unofficial Telegram Desktop client
Source0:  %{url}/releases/download/v%{version}/%{appname}-%{version}-full.tar.gz

Patch2:   %{pgr}/0001-tdesktop-use-system-font-by-default.patch
Patch3:   %{pgr}/0001-tdesktop-remove-default-font-in-settings.patch
Patch100: %{pgr}/1000-tgcalls-fix-libyuv-include.patch
Patch101: %{pgr}/1000-lib_tl-fix-cstring-include.patch
Patch110: %{pgr}/1000-tdesktop-fix-build-qt5.patch
Patch201: %{pgr}/0001-window-set-minimum-width-to-360px.patch
Patch204: %{pgr}/0001-tdesktop-use-native-window-frame.patch

Patch200: %{cmt}/1001-revert-hidpi-handling.patch



# Telegram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
%if %{undefined arm64}
  %define arm64 aarch64
%endif
%if %{undefined x86_64}
  %define x86_64 x86_64
%endif
%if %{undefined riscv64}
  %define riscv64 riscv64
%endif
ExclusiveArch: %x86_64 %arm64 ppc64le %riscv64

# for cppgir generator
BuildRequires: python3-rpm-macros

%if %{with qt5}
BuildRequires: (qt5-srpm-macros or libqt5-qtbase-common-devel)
%else
BuildRequires: (qt6-srpm-macros or qt6-macros)
%endif

BuildRequires: cmake(Microsoft.GSL) >= 4.0.0-10
BuildRequires: cmake(OpenAL)
%if %{with qt5}
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5OpenGL)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5WaylandClient)
BuildRequires: cmake(Qt5WaylandCompositor)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5QuickWidgets)
BuildRequires: cmake(KF5CoreAddons)
%else
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: cmake(Qt6WaylandCompositor)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(KF6CoreAddons)
%endif
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
BuildRequires: cmake(rlottie)

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.68) >= 2.77.0
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(webkitgtk-6.0)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)
BuildRequires: pkgconfig(xkbcommon)

BuildRequires: cmake
BuildRequires: desktop-file-utils

#ffmpeg related
BuildRequires: pkgconfig(libavcodec) = 60.31.102
BuildRequires: pkgconfig(libavdevice) = 60.3.100
BuildRequires: pkgconfig(libavfilter) = 9.12.100
BuildRequires: pkgconfig(libavformat) = 60.16.100
BuildRequires: pkgconfig(libavutil) = 58.29.100
BuildRequires: pkgconfig(libpostproc) = 57.3.100
BuildRequires: pkgconfig(libswresample) = 4.12.100
BuildRequires: pkgconfig(libswscale) = 7.5.100

%if 0%{suse_version} > 0
BuildRequires: libboost_regex-devel
%else
BuildRequires: ffmpeg-free-devel
BuildRequires: libatomic
%endif

BuildRequires: (libqrcodegencpp-devel or QR-Code-generator-devel)
BuildRequires: (libappstream-glib or appstream-glib)

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libdispatch-devel
BuildRequires: libstdc++-devel
BuildRequires: python3
BuildRequires: python3dist(packaging)
BuildRequires: boost-devel
BuildRequires: fmt-devel
BuildRequires: gobject-introspection-devel
%if %{with qt5}
BuildRequires: (qt5-qtbase-private-devel or libqt5-qtbase-private-headers-devel)
%else
BuildRequires: (qt6-qtbase-private-devel or qt6-base-private-devel)
%endif


BuildRequires: dos2unix
BuildRequires: binutils
BuildRequires: upx
BuildRequires: coreutils
BuildRequires: sed

%if 0%{suse_version} == 0
%if %{with qt5}
Requires: qt5-qtbase%{?_isa} = %{_qt5_version}
Requires: qt5-qtimageformats%{?_isa} = %{_qt5_version}
%else
Requires: qt6-qtbase%{?_isa} = %{_qt6_version}
Requires: qt6-qtimageformats%{?_isa} = %{_qt6_version}
%endif
Recommends: webkitgtk6.0%{?_isa}
%else
Recommends: WebKitGTK-6.0
%endif

# Short alias for the main package...
Provides: telegram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: telegram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Virtual provides for bundled libraries...
Provides: bundled(cld3) = 3.0.13~gitb48dc46
Provides: bundled(libtgvoip) = 2.4.4~gite286ab6
Provides: bundled(tgcalls) = 0~g871ea04
Provides: bundled(plasma-wayland-protocols) = 1.10.0
Provides: bundled(libprisma) = 0~gitadf35ba

%description
Telegram is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any number of your phones,
tablets or computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 50,000 people or
channels for broadcasting to unlimited audiences. You can write to your
phone contacts and find people by their usernames. As a result, Telegram is
like SMS and email combined — and can take care of all your personal or
business messaging needs.

%prep
# Unpacking Telegram Desktop source archive...
%autosetup -n %{appname}-%{version}-full -p1 -N

# Unbundling libraries...
for i in Telegram/{ThirdParty/{GSL,QR,dispatch,expected,fcitx-qt5,fcitx5-qt,hime,hunspell,scudo,kimageformats,kcoreaddons,lz4,minizip,nimf,range-v3,xxHash,rlottie},lib_ui/fonts/*.ttf}
do
rm -rf "$i" ||:
done

# 64Gram: fix inconsistent line ending
dos2unix LICENSE LEGAL features.md changelog.txt README.md lib/xdg/*
find . -not -type d -exec file "{}" ";" -print0 | grep -z CRLF | cut -d':' -z -f1 | xargs -0 dos2unix

%autopatch -p1

%build
# Building Telegram Desktop using cmake...
%cmake \
    -DTDESKTOP_API_ID=611335 \
    -DTDESKTOP_API_HASH=d524b414d21f4d37f08684c1df41ac9c \
    -DTDESKTOP_DISABLE_AUTOUPDATE:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_RLOTTIE:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON
%cmake_build

%install
%cmake_install

%if 0%{suse_version} > 0
%define dr %{_builddir}/%{appname}-%{version}-full
for i in README.md changelog.txt features.md; do
  install -Dm644 %{dr}/$i %{buildroot}%{_defaultdocdir}/%{name}/$i
done
for i in LICENSE LEGAL; do
  install -Dm644 %{dr}/$i %{buildroot}%{_defaultlicensedir}/%{name}/$i
done
%endif
%define br %{buildroot}%{_bindir}

#(
#echo '%package dependencies';
#echo "cat << 'EOFEOF'"
#echo %{br}/telegram-desktop | %{__find_requires_basic}
#echo 'EOFEOF'
#echo %{__find_requres_basic}
#echo 'Dependencies for 64gram.'
#echo '%files dependencies'
#) | tee %{__find_requires}

strip -s %{br}/telegram-desktop
#upx -9 %{br}/telegram-desktop -o%{br}/64Gram
#rm %{br}/telegram-desktop

#post
#{_sbindir}/update-alternatives --install '%{_bindir}/telegram-desktop' telegram-desktop '%{_bindir}/64Gram' 25 || :

#postun
#{_sbindir}/update-alternatives --remove telegram-desktop '%{_bindir}/64Gram' || :

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%doc README.md changelog.txt features.md
%license LICENSE LEGAL
%{_bindir}/telegram-desktop
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Tue Jul 23 2024 huakim tylyktar <zuhhaga@gmail.com> - 1.1.31-1
- new version
- Fix dependency resolve
