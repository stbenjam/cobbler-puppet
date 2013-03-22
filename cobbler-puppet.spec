Name:		cobbler-puppet
Version:	1.0
Release:	0
Summary:	Tool for importing cobbler system profiles from an ENC

Group:	    Applications/System	
License:	MIT
URL:		https://github.com/stbenjam/cobbler-puppet
Source0:	cobbler-puppet.tar.gz

Requires:	python PyYAML

%description
Tool for importing cobbler system profiles from an ENC


%prep
%setup -n src

%build
%{__python} setup.py build

%install
test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --optimize=1 --root=$RPM_BUILD_ROOT $PREFIX
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/etc
install -m 0755 cobbler-import-enc ${RPM_BUILD_ROOT}/usr/bin
install -m 0600 etc/cobbler-puppet.conf ${RPM_BUILD_ROOT}/etc

%files
%defattr(-,root,root,-)
%{python_sitelib}/cobbler_puppet
/usr/bin/cobbler-import-enc
%config(noreplace) /etc/cobbler-puppet.conf
%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%{python_sitelib}/cobbler*.egg-info
%endif

%changelog
* Fri Mar 22 2013 Stephen Benjamin <skbenja@gmail.com>
- Initial creation
