%define name 	viewmol
%define version 2.4.1
%define release %mkrel 10

Summary: 	Molecule viewer and editor
Name: 		%name
Version: 	%version
Release: 	%release
License: 	GPL
Group: 		Sciences/Chemistry
URL: 		http://viewmol.sourceforge.net
BuildRoot: 	%_tmppath/%name-%version-buildroot
Source: 	%name-%version.src.tar.bz2
BuildRequires: 	libtiff-devel mesaglu-devel libpython-devel
BuildRequires: 	libx11-devel x11-proto-devel libxt-devel libxi-devel libxmu-devel
BuildRequires:  lesstif-devel png-devel

%description
Viewmol is a graphical front end for computational chemistry programs.
It is able to graphically aid in the generation of molecular structures
for computations and to visualize their results. At present Viewmol
includes input filters for Discover, DMol, Gamess, Gaussian 9x, Gulp,
Mopac, and Turbomole outputs as well as for PDB files.

%prep
%setup -q -n %name-%version
cd source
#tar xfj %{SOURCE}
perl -p -i -e 's!usr/local/lib!%_libdir!g' getrc.c
perl -p -i -e 's!lib/viewmol!%_lib/viewmol!g' install

%build
cd source
mkdir Linux
echo "LIBTIFF = -L%_libdir" > .config.Linux
echo "TIFFINCLUDE = /usr/include" >> .config.Linux
echo "MESALIB = -L/usr/%_lib" >> .config.Linux
echo "MESAINCLUDE = /usr/include/GL" >> .config.Linux
#echo "PYTHONVERSION = %pythonver" >> .config.Linux
echo "PYTHONINCLUDE = /usr/include/python%pyver" >> .config.Linux
echo "LIBPYTHON = -L%_libdir/python%pyver" >> .config.Linux
cd Linux
cat ../.config.Linux > makefile
echo 'COMPILER = gcc' >> makefile
echo 'OPT=${RPM_OPT_FLAGS}' >> makefile
echo 'CFLAGS=-Wall -I/usr/include -DLINUX' >> makefile
echo 'LDFLAGS=' >> makefile
echo 'SCANDIR=' >> makefile
echo 'INCLUDE=$(MESAINCLUDE) -I$(TIFFINCLUDE) -I$(PYTHONINCLUDE)' >> makefile
echo 'LIBRARY=$(MESALIB) $(LIBPYTHON)' >> makefile
echo 'LIBS=-L/usr/%_lib -lpython%pyver -ltiff -lGLU -lGL -lpng -lXm -lXmu -lXt -lX11 -lXi' >> makefile
cat ../Makefile >> makefile
make viewmol_
make tm_
make bio_
make readgamess_
make readgauss_
make readmopac_
make readpdb_

%install
rm -Rf $RPM_BUILD_ROOT
cd source
./install $RPM_BUILD_ROOT%_prefix
mkdir -p $RPM_BUILD_ROOT%_docdir
mkdir -p $RPM_BUILD_ROOT%_docdir/%name-%version
mv $RPM_BUILD_ROOT/%_libdir/viewmol/doc/* $RPM_BUILD_ROOT%_docdir/%name-%version
rmdir $RPM_BUILD_ROOT/%_libdir/viewmol/doc
chmod 755 $RPM_BUILD_ROOT/%_libdir/viewmol/Linux/*
chmod 755 $RPM_BUILD_ROOT/%_bindir/*

# menu

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=ViewMol
Comment=GUI interface for chemistry software
Exec=%{_bindir}/%{name} 
Icon=chemistry_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Motif;Education;Science;Chemistry;
EOF

%if %mdkversion < 200900
%post 
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -fr %buildroot

%files
%defattr(-,root,root,0755)
%doc %_docdir/%name-%version
%_bindir/%name
%_libdir/%name
%_datadir/applications/mandriva-%name.desktop

