%define dtdver 4.1.2
%define mltyp xml

%define name docbook-dtd412-xml
%define version 1.0
%define release %mkrel 23

Name:    %{name}
Version: %{version}
Release: %{release}
Group  : Publishing

Summary: XML document type definition for DocBook %{dtdver}

License: Artistic style
URL    : http://www.oasis-open.org/docbook/

Provides: docbook-dtd-%{mltyp}
Requires: coreutils
Requires: sgml-common >= 0.6.3-2mdk
Requires: libxml2-utils

BuildRoot: %_tmppath/%name-buildroot

# Zip file downloadable at http://www.oasis-open.org/docbook/%{mltyp}/%{dtdver}
Source0  : docbkx412.tar.bz2 
Source1  : docbook-dtd412-xml-catalog.tar.bz2
Patch0   : %{name}-%{version}.catalog.patch
Patch1   : %{name}-%{version}.dbcentx.patch
BuildArch: noarch  


%define sgmlbase %{_datadir}/sgml

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.


%prep
%setup -q
%setup -D -a 1 -q
%patch0 -p1
%patch1 -p1

%build


%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
mkdir -p $DESTDIR
install -m644 docbook.cat $DESTDIR/catalog
install -m644 xmlcatalog $DESTDIR
install -m644 *.dtd $DESTDIR
install -m644 *.mod $DESTDIR

# Symlinks
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml
ln -s %{mltyp}-docbook-%{dtdver}.cat \
	$RPM_BUILD_ROOT%{_sysconfdir}/sgml/%{mltyp}-docbook.cat

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# What's that for?
# touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/catalog


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root)
%doc *.txt ChangeLog
%dir %{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
%{_sysconfdir}/sgml/xml-docbook.cat
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# rpmlint complains about this and indeed seems unnecesary
# %ghost %config(noreplace) %{_sysconfdir}/sgml/catalog

#fix buggy XML catalog unregistration which was present in postun script
#for all versions before 1.0-10mdk
%triggerpostun -- docbook-dtd412-xml < 1.0-10mdk
CATALOG=%{sgmlbase}/docbook/xmlcatalog

%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML" \
	"file:///usr/share/sgml/docbook/xml-dtd-4.1.2/xmlcatalog" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://www.oasis-open.org/docbook/xml/4.1.2" \
	"xml-dtd-4.1.2" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://www.oasis-open.org/docbook/xml/4.1.2" \
	"xml-dtd-4.1.2" $CATALOG

#fix old buggy postun
%triggerpostun -- docbook-dtd412-xml < 1.0-15mdk
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi


%Post
##
## SGML catalog
##
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi

##
## XML catalog
##

CATALOG=%{sgmlbase}/docbook/xmlcatalog

%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML" \
	"file:///usr/share/sgml/docbook/xml-dtd-4.1.2/xmlcatalog" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://www.oasis-open.org/docbook/xml/4.1.2" \
	"xml-dtd-4.1.2" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://www.oasis-open.org/docbook/xml/4.1.2" \
	"xml-dtd-4.1.2" $CATALOG

%Postun
# test xmlcatalog is available before using it...
if [ -x %{_bindir}/xmlcatalog ]; then 
##
## SGML catalog
##
# Do not remove if upgrade
if [ "$1" = "0" ]; then
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e %{sgmlbase}/openjade/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/openjade/catalog
  fi

  if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/docbook/dsssl-stylesheets/catalog
  fi

##
## XML catalog
##

  CATALOG=%{sgmlbase}/docbook/xmlcatalog

  if [ -f $CATALOG ]; then

    %{_bindir}/xmlcatalog --noout --del \
	    "-//OASIS//DTD DocBook XML" $CATALOG
    %{_bindir}/xmlcatalog --noout --del \
	    "xml-dtd-4.1.2" $CATALOG
  fi
fi
fi

 
