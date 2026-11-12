#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	josepy
Summary:	JOSE protocol implementation
Summary(pl.UTF-8):	Implementacja protokołu JOSE
Name:		python3-%{module}
Version:	2.3.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/j/josepy/josepy-%{version}.tar.gz
# Source0-md5:	16c3374ae6c8a81a78f0bd56698ae07d
URL:		https://josepy.readthedocs.io/en/latest/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-installer
BuildRequires:	python3-poetry-core >= 2.2.0
%if %{with tests}
BuildRequires:	python3-cryptography >= 1.5
BuildRequires:	python3-pytest >= 2.8.0
BuildRequires:	python3-pytest-cov
%endif
%if %{with doc}
BuildRequires:	python3-Sphinx >= 4.3.0
BuildRequires:	python3-cryptography >= 1.5
BuildRequires:	python3-sphinx_rtd_theme >= 1.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.10
Conflicts:	python-josepy < 1.13.0-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides JOSE protocol implementation.

%description -l pl.UTF-8
Ten pakiet zawiera implementację protokołu JOSE.

%package apidocs
Summary:	API documentation for josepy module
Summary(pl.UTF-8):	Dokumentacja API modułu josepy
Group:		Documentation

%description apidocs
API documentation for josepy module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu josepy.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD="%{__python3} -m sphinx"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jws{,-3}
ln -sf jws-3 $RPM_BUILD_ROOT%{_bindir}/jws

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%attr(755,root,root) %{_bindir}/jws-3
%{_bindir}/jws
%{py3_sitescriptdir}/josepy
%{py3_sitescriptdir}/josepy-%{version}.dist-info

%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,man,*.html,*.js}
