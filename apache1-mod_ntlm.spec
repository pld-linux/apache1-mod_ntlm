# TODO: review security issues
%define		mod_name	ntlm
%define 	apxs		/usr/sbin/apxs1
Summary:	This is the NTLM authentication module for Apache
Summary(pl.UTF-8):	Moduł uwierzytelnienia NTLM dla Apache
Name:		apache1-mod_%{mod_name}
Version:	0.4
Release:	0.4
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modntlm/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	5e9b8d1abf872926d6ff01a05a7deb2a
Patch0:		%{name}-security.patch
URL:		http://modntlm.sourceforge.net/
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_ntlm <= 1:0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using samba or windows-like server (using
NTLM protocol).

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP poprzez sambę lub serwer na Windows (z
użyciem protokołu NTLM).

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make} APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
