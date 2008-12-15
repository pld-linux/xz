#
# Conditional build:
%bcond_without	tests	# don't perform make check
#
%define	snap	alpha
Summary:	LZMA Encoder/Decoder
Summary(pl.UTF-8):	Koder/Dekoder LZMA
Name:		lzma
Version:	4.999.5
Release:	0.%{snap}.3
Epoch:		1
License:	LGPL v2.1+, helper scripts on GPL v2+
Group:		Applications/Archiving
Source0:	http://tukaani.org/lzma/%{name}-%{version}%{snap}.tar.gz
# Source0-md5:	db736e080858a7c34357960254dda280
Patch0:		%{name}-memlimit.patch
URL:		http://tukaani.org/lzma/
BuildRequires:	rpmbuild(macros) >= 1.402
BuildRequires:	sed >= 4.0
Suggests:	mktemp
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

%description libs
LZMA shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona LZMA.

%package devel
Summary:	Header file for LZMA library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki LZMA
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header file for LZMA library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki LZMA.

%package static
Summary:	LZMA static library
Summary(pl.UTF-8):	Biblioteka statyczna LZMA
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
LZMA static library.

%description static -l pl.UTF-8
Biblioteka statyczna LZMA.

%prep
%setup -q -n %{name}-%{version}%{snap}
%patch0 -p1
sed -i 's|/usr/bin/mktemp|/bin/mktemp|' scripts/lzdiff

%build
%configure

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/env.d,%{_lib}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/liblzma.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/liblzma.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/liblzma.so

echo '#LZMA_OPT="--threads=2"' > $RPM_BUILD_ROOT/etc/env.d/LZMA_OPT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/LZMA_OPT
%attr(755,root,root) %{_bindir}/*lz*
%{_mandir}/man1/lz*.1*

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README THANKS TODO
%doc doc/{bugs,faq,file-format,history,lzma-intro}.txt
%attr(755,root,root) /%{_lib}/liblzma.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/liblzma.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/liblzma-*.txt
%attr(755,root,root) %{_libdir}/liblzma.so
%{_libdir}/liblzma.la
%{_includedir}/lzma.h
%{_includedir}/lzma
%{_pkgconfigdir}/lzma.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblzma.a
