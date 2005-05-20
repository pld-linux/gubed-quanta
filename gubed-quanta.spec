Summary:	Gubed PHP Debugger: Quanta support
Summary(pl):	Gubed PHP Debugger - wsparcie dla Quanty
Name:		gubed-quanta
Version:	3.4
Release:	0.5
Epoch:		0
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/gubed/GubedQuanta%(echo %{version} | tr . _).tar.gz
# Source0-md5:	1cca80dc0f47602231f4d2b91a8d296a
Source1:	%{name}-localsettings.php
URL:		http://gubed.mccabe.nu/
BuildRequires:	sed >= 4.0
Requires:	php >= 3:4.3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/GubedQuanta
%define		_sysconfdir	/etc/gubed

%description
Gubed PHP Debugger is a program to debug PHP scripts. It currently
supports stepping through code, watching contents of variables and
setting breakpoints (line and conditional). No changes are needed to
server software or scripts being debugged.

This package contains support for Quanta.

%description -l pl
Gubed PHP Debugger to program do odpluskwiania skryptów PHP. Aktualnie
obs³uguje krokowe wykonywanie kodu, ¶ledzenie zawarto¶ci zmiennych i
ustawianie pu³apek (w danej linii lub warunkowych). Nie wymaga zmian w
oprogramowaniu serwera ani odpluskwianych skryptach.

Ten pakiet zawiera wsparcie dla Quanty.

%prep
%setup -q -n GubedQuanta%(echo %{version} | tr . _)
sed Gubed/GubedGlobals.php -i -e \
	"s,dirname(__FILE__).'/localsettings.php','%{_sysconfdir}/localsettings.php',g"

rm -f docs/license.txt # Pure GPL

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cd Gubed
cp -a *.php gbdNoDebug.txt $RPM_BUILD_ROOT%{_appdir}
cp -a */ $RPM_BUILD_ROOT%{_appdir}

cat >> $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf <<EOF
<IfModule mod_alias.c>
    Alias /Gubed %{_appdir}
</IfModule>
<Directory %{_appdir}>
    <IfModule mod_access.c>
        order allow,deny
        allow from 127.0.0.1
    </IfModule>
</Directory>
# vim: filetype=apache ts=4 sw=4 et
EOF

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/localsettings.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-%{name}.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/GubedTest
%{_appdir}/develop
%{_appdir}/*.txt
%{_appdir}/*.php
