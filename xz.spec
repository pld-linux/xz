#
# Conditional build:
%bcond_without	tests	# don't perform make check
%bcond_without	asm	# ix86 asm optimizations

%ifnarch %{ix86}
# Speed-optimized CRC64 using slicing-by-four algorithm. This uses only i386
# instructions, but it is optimized for i686 and later (including e.g. Pentium
# II/III/IV, Athlon XP, and Core 2).
%undefine	with_asm
%endif

%if "%{pld_release}" == "ac"
%undefine	with_asm
%endif

Summary:	LZMA Encoder/Decoder
Summary(pl.UTF-8):	Koder/Dekoder LZMA
Name:		xz
Version:	5.0.2
Release:	1
Epoch:		1
License:	LGPL v2.1+, helper scripts on GPL v2+
Group:		Applications/Archiving
Source0:	http://tukaani.org/xz/%{name}-%{version}.tar.bz2
# Source0-md5:	ee05b17a4062bb55cba099ef46eca007
URL:		http://tukaani.org/xz/
%{?with_asm:BuildRequires:	gcc >= 5:3.4}
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.402
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Suggests:	mktemp
Provides:	lzma = %{epoch}:%{version}-%{release}
Obsoletes:	lzma < 1:4.999.6
Conflicts:	rpm < 4.4.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LZMA is default and general compression method of 7z format in 7-Zip
program. LZMA provides high compression ratio and very fast
decompression, so it is very suitable for embedded applications. For
example, it can be used for ROM (firmware) compressing.

LZMA features:

- Compressing speed: 500 KB/s on 1 GHz CPU
- Decompressing speed:
  - 8-12 MB/s on 1 GHz Intel Pentium 3 or AMD Athlon.
  - 500-1000 KB/s on 100 MHz ARM, MIPS, PowerPC or other simple RISC
    CPU.
- Small memory requirements for decompressing: 8-32 KB + dictionary
  size
- Small code size for decompressing: 2-8 KB (depending from speed
  optimizations)

%description -l pl.UTF-8
LZMA jest domyślnym i ogólnym algorytmem kompresji formatu 7z
stosowanego przez 7-Zip. LZMA zapewnia wysoki stopień kompresji i
bardzo szybką dekompresję, więc nadaje się do zastosowań osadzonych.
Przykładowo, może być użyty do kompresji ROM-u (firmware'u).

Cechy LZMA:

- Szybkość kompresowania: 500 KB/s na 1 GHz procesorze,
- Szybkość dekompresowania:
  - 8-12 MB/s na 1 GHz Pentium 3 lub Athlonie,
  - 500-1000 KB/s na 100 MHz procesorach ARM, MIPS, PowerPC lub innych
    prostych RISC-ach,
- Mała ilość pamięci potrzebna do dekompresowania: 8-32 KB + rozmiar
  słownika,
- Mały rozmiar kodu dekompresującego: 2-8 KB (w zależności od opcji
  optymalizacji).

%package libs
Summary:	LZMA shared library
Summary(pl.UTF-8):	Biblioteka współdzielona LZMA
Group:		Libraries
Provides:	lzma-libs = %{epoch}:%{version}-%{release}
Obsoletes:	lzma-libs < 1:4.999.6

%description libs
LZMA shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona LZMA.

%package devel
Summary:	Header file for LZMA library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki LZMA
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Provides:	lzma-devel = %{epoch}:%{version}-%{release}
Obsoletes:	lzma-devel < 1:4.999.6

%description devel
Header file for LZMA library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki LZMA.

%package static
Summary:	LZMA static library
Summary(pl.UTF-8):	Biblioteka statyczna LZMA
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lzma-static = %{epoch}:%{version}-%{release}
Obsoletes:	lzma-static < 1:4.999.6

%description static
LZMA static library.

%description static -l pl.UTF-8
Biblioteka statyczna LZMA.

%prep
%setup -q

%build
%configure \
	%{!?with_asm:--disable-assembler}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/env.d,%{_lib}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/liblzma.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/liblzma.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/liblzma.so

echo '#XZ_OPT="--threads=2"' > $RPM_BUILD_ROOT/etc/env.d/XZ_OPT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/XZ_OPT
%attr(755,root,root) %{_bindir}/lz*
%attr(755,root,root) %{_bindir}/unlzma
%attr(755,root,root) %{_bindir}/unxz
%attr(755,root,root) %{_bindir}/xz*
%{_mandir}/man1/lz*.1*
%{_mandir}/man1/unlzma.1*
%{_mandir}/man1/unxz.1*
%{_mandir}/man1/xz*.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING README THANKS
%doc doc/*.txt
%attr(755,root,root) /%{_lib}/liblzma.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/liblzma.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblzma.so
%{_libdir}/liblzma.la
%{_includedir}/lzma.h
%{_includedir}/lzma
%{_pkgconfigdir}/liblzma.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblzma.a
