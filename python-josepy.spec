#
# Conditional build:
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module
#
%define 	module	josepy
Summary:	JOSE protocol implementation
Name:		python-%{module}
Version:	1.1.0
Release:	3
License:	Apache v2.0
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/j/josepy/josepy-%{version}.tar.gz
# Source0-md5:	b582dbfd70ccdbe5926e4dc46ba6719c
URL:		https://josepy.readthedocs.io/en/latest/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides JOSE protocol implementation.

%package -n python3-%{module}
Summary:	JOSE protocol implementation in Python 3
Group:		Development/Languages/Python

%description -n python3-%{module}
This package provides JOSE protocol implementation in Python 3.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jws
%{py_sitescriptdir}/josepy-*-py*.egg-info
%{py_sitescriptdir}/josepy
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/josepy-*-py*.egg-info
%{py3_sitescriptdir}/josepy
%endif
