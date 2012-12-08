%define dtdver 4.1.2
%define mltyp xml

%define name docbook-dtd412-xml
%define version 1.0
%define release %mkrel 28

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
rm -rf %{buildroot}
DESTDIR=%{buildroot}%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
mkdir -p $DESTDIR
install -m644 docbook.cat $DESTDIR/catalog
install -m644 xmlcatalog $DESTDIR
install -m644 *.dtd $DESTDIR
install -m644 *.mod $DESTDIR

# Symlinks
mkdir -p %{buildroot}%{_sysconfdir}/sgml
ln -s %{mltyp}-docbook-%{dtdver}.cat \
	%{buildroot}%{_sysconfdir}/sgml/%{mltyp}-docbook.cat

mkdir -p %{buildroot}%{_sysconfdir}/sgml
touch %{buildroot}%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# What's that for?
# touch %{buildroot}%{_sysconfdir}/sgml/catalog


%clean
rm -rf %{buildroot}


%files
%defattr (-,root,root)
%doc *.txt ChangeLog
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

 


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-27mdv2011.0
+ Revision: 663817
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-26mdv2011.0
+ Revision: 604802
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-25mdv2010.1
+ Revision: 520687
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-24mdv2010.0
+ Revision: 413365
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.0-23mdv2009.1
+ Revision: 350814
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0-22mdv2009.0
+ Revision: 220670
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0-21mdv2008.1
+ Revision: 149188
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 16 2007 Thierry Vignaud <tv@mandriva.org> 1.0-20mdv2008.0
+ Revision: 64213
- rebuild

* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-19mdv2008.0
+ Revision: 18831
- clean spec; rebuild for new era


* Tue Mar 21 2006 Camille Begnis <camille@mandriva.com> 1.0-18mdk
- rebuild
- change requires syntax

* Tue Nov 23 2004 Camille Begnis <camille@mandrakesoft.com> 1.0-17mdk
- added Prereq: libxml2-utils [Bug 12470]
- remove unnecesary ghost file /etc/sgml/catalog

* Mon Aug 16 2004 Camille Begnis <camille@mandrakesoft.com> 1.0-16mdk
- rebuild

* Mon Jul 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-15mdk
- Add some ghost/config files to package
- Fix upgrade

* Fri Jul 18 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-14mdk
- Fix uninstall : only unregister from existing catalog

