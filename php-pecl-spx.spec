#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	spx
Summary:	SPX - A simple profiler for PHP
Name:		%{php_name}-pecl-%{modname}
Version:	0.4.7
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://github.com/NoiseByNorthwest/php-spx/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	599bd8812d1abbf804af8dc47c967c71
URL:		https://github.com/NoiseByNorthwest/php-spx
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-devel >= 4:5.6
BuildRequires:	rpmbuild(macros) >= 1.666
BuildRequires:	zlib-devel
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A simple & straight-to-the-point PHP profiling extension with its
built-in web UI.

%prep
%setup -qn php-%{modname}-%{version}

%build
phpize
%configure
%{__make}

# simple module load test
%{__php} -n -q \
	-d extension_dir=modules \
	-d extension=%{modname}.so \
	-r 'exit(extension_loaded("%{modname}") ? 0 : 1);'

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README.md
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_datadir}/misc/php-spx
