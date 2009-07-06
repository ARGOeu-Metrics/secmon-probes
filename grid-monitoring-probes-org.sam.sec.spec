%define site org.sam.sec
%define dir %{_libexecdir}/grid-monitoring/probes/%{site}

%define debug_package %{nil}

Summary: WLCG Compliant Probes from %{site}
Name: grid-monitoring-probes-org.sam.sec
Version: 0.1.0
Release: 1%{?dist}

License: GPL
Group: Network/Monitoring
Source0: %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: grid-monitoring-probes-org.sam > 0.1.4-5
AutoReqProv: no
BuildArch: noarch
BuildRequires: python >= 2.3

%description
Contains the following Nagios probes: 
WN-pakiti
- Metrics results from WNs are sent to configured pakiti server(s). Message Broker gets as result whether the client reported correctly to the server(s).

%prep
%setup -q

%build

%install
export DONT_STRIP=1
%{__rm} -rf %{buildroot}
install --directory %{buildroot}%{dir}
%{__cp} -rpf .%dir/wnjob  %{buildroot}%{dir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{dir}/wnjob
%{dir}

%changelog
* Mon Jul 6 2009 C. Triantafyllidis <ctria@grid.auth.gr> - 0.1.0-1
- Initial build
- Based on CE-probe WN tarball assembly 
  * grid-monitoring-probes-org.sam > 0.1.4-5
- Contains probes:
  * WN-Pakiti
