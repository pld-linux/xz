Summary:	LZMA Encoder/Decoder
Summary(pl):	Koder/Dekoder LZMA
Name:		lzma
Version:	4.27
Release:	1
License:	LGPL
Group:		Applications/Archiving
Source0:	http://dl.sourceforge.net/sevenzip/%{name}427.tar.bz2
# Source0-md5:	8e99976772e28c6fa3c5d9a2fb82ca50
Patch0:		%{name}-quiet.patch
Patch1:		%{name}427_zlib.patch
URL:		http://www.7-zip.org/sdk.html
BuildRequires:	gcc >= 5:3.4.0
BuildRequires:	libstdc++-devel
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
- Small memory requirements for decompressing: 8-32 KB
- Small code size for decompressing: 2-8 KB (depending from speed
  optimizations)

%description -l pl
LZMA jest domy¶lnym i ogólnym algorytmem kompresji formatu 7z
stosowanego przez 7-Zip. LZMA zapewnia wysoki stopieñ kompresji i
bardzo szybk± dekompresjê, wiêc nadaje siê do zastosowañ osadzonych.
Przyk³adowo, mo¿e byæ u¿yty do kompresji ROM-u (firmware'u).

Cechy LZMA:

- Szybko¶æ kompresowania: 500 KB/s na 1 GHz procesorze,
- Szybko¶æ dekompresowania:
  - 8-12 MB/s na 1 GHz Pentium 3 lub Athlonie,
  - 500-1000 KB/s na 100 MHz procesorach ARM, MIPS, PowerPC lub innych
    prostych RISC-ach,
- Ma³a ilo¶æ pamiêci potrzebna do dekompresowania: 8-32 KB,
- Ma³y rozmiar kodu dekompresuj±cego: 2-8 KB (w zale¿no¶ci od opcji
  optymalizacji).

%package devel
Summary:        LZMA library
Summary(pl):	Biblioteka LZMA
Group:          Development/Libraries

%description devel
LZMA Library.

%description devel -l pl
Biblioteka LZMA.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

%build
cd SRC/7zip/Compress/LZMA_Alone

%{__make} -f makefile.gcc
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fprofile-generate -c -I ../../.." \
	LDFLAGS="%{rpmldflags}" \
	LIB="-lm -lgcov"

cat ../LZMA/* > test1
cat lzma *.o > test2
./lzma e test1 test3
./lzma e test2 test4
./lzma d test3 test5
./lzma d test4 test6

%{__make} -f makefile.gcc clean

%{__make} -f makefile.gcc \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fprofile-use -c -I ../../.." \
	LDFLAGS="%{rpmldflags}"

cd ../LZMA_Lib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

install SRC/7zip/Compress/LZMA_Alone/lzma $RPM_BUILD_ROOT%{_bindir}
install SRC/7zip/Compress/LZMA_Lib/liblzma.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc history.txt lzma.txt
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblzma.a
