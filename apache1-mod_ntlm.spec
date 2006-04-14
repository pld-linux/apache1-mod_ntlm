# TODO: review security issues
%define		mod_name	ntlm
%define 	apxs		/usr/sbin/apxs1
Summary:	This is the NTLM authentication module for Apache
Summary(pl):	Modu³ uwierzytelnienia NTLM dla Apache
Name:		apache1-mod_%{mod_name}
Version:	0.4
Release:	0.3
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modntlm/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	5e9b8d1abf872926d6ff01a05a7deb2a
Patch0:		%{name}-security.patch
URL:		http://modntlm.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_%{mod_name} <= 1:0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using samba or windows-like server (using
NTLM protocol).

%description -l pl
To jest modu³ uwierzytelnienia dla Apache pozwalaj±cy na
uwierzytelnianie klientów HTTP poprzez sambê lub serwer na Windows (z
u¿yciem protoko³u NTLM).

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch -p1

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
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
