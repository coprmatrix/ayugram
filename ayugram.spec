%{!?_metainfodir:%define _metainfodir %{_datadir}/metainfo}

# Telegram Desktop's constants...
%global appname ayugram

# Reducing debuginfo verbosity...
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

Name: %{appname}
Version: 5.12.3
Release: 0%{?dist}

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * cld3  - Apache-2.0 -- static dependency;
# * libprisma - MIT -- static dependency;
# * tgcalls - LGPL-3.0-only -- static dependency;
# * plasma-wayland-protocols - LGPL-2.1-or-later -- static dependency;
# * wayland-protocols - MIT -- static dependency;
License:  GPL-3.0-or-later AND Apache-2.0 AND LGPL-3.0-only AND LGPL-2.1-or-later AND MIT
URL:      https://github.com/ayugram/ayugramdesktop

Summary:  Unofficial Telegram Desktop client
Source0:  %{name}-%{version}.tar.gz

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
BuildRequires: qt6-srpm-macros
BuildRequires: cmake(Microsoft.GSL) >= 4.0.0-10
BuildRequires: cmake(ada)
BuildRequires: cmake(OpenAL)
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
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
#BuildRequires: cmake(rlottie)
BuildRequires: cmake(Td)
BuildRequires: cmake(fmt)
BuildRequires: cmake(qrcodegencpp)
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
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavdevice)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libpostproc)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)
BuildRequires: tdlib-static
BuildRequires: tdlib-devel
BuildRequires: openssl-devel-engine
BuildRequires: libatomic
BuildRequires: pkgconfig(qrcodegencpp)
BuildRequires: libappstream-glib
BuildRequires: gcc
BuildRequires: ccache
BuildRequires: gcc-c++
BuildRequires: libdispatch-devel
BuildRequires: libstdc++-devel
BuildRequires: python3
BuildRequires: python3dist(packaging)
BuildRequires: boost-devel
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: qt6-qtbase-private-devel
BuildRequires: dos2unix
BuildRequires: binutils
BuildRequires: upx
BuildRequires: coreutils
BuildRequires: sed

Requires: qt6-qtbase%{?_isa}
Requires: qt6-qtimageformats%{?_isa}

# Short alias for the main package...
Provides: telegram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: telegram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

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
%autosetup -n %{appname}-%{version} -p1

%autopatch -p1

%build
# Building Telegram Desktop using cmake...
%cmake \
    -DTDESKTOP_API_ID=611335 \
    -DTDESKTOP_API_HASH=d524b414d21f4d37f08684c1df41ac9c \
    -DTDESKTOP_DISABLE_AUTOUPDATE:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_RLOTTIE:BOOL=OFF \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON
%cmake_build

%install
%cmake_install

%check

%files
%doc README.md changelog.txt features.md
%license LICENSE LEGAL
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Tue Jul 23 2025 huakim tylyktar <zuhhaga@gmail.com> - 1.1.31-1
- new version
- Fix dependency resolve
