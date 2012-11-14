%define site eu.egi.sec
%define dir %{_libexecdir}/grid-monitoring/probes/%{site}

%define debug_package %{nil}

Summary: Security monitoring probes based on EGI CSIRT requirements
Name: grid-monitoring-probes-eu.egi.sec
Version: 1.0.6
Release: 4%{?dist}

License: ASL 2.0
Group: Applications/System
Source0: %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: grid-monitoring-probes-org.sam > 0.1.4-5
AutoReqProv: no
BuildArch: noarch
Obsoletes: grid-monitoring-probes-org.sam.sec

%description
This package includes the framework to submit grid jobs to monitor the security of the EGI sites.
Special care has been taken so that results of the probes are transmitted back to the Nagios server using a secure channel.

Currently it supports the following middlewares:
- gLite
- ARC

Additionally it contains the following Nagios probes: 
* WN-pakiti
- Pakiti results from the tested WN are sent to configured pakiti server(s). The probe reports to Nagios whether the reporting to Pakiti server(s) was successful.
* WN-CRL
- Tests the CRLs validity on WN.
* WN-Permissions
- Checks the permissions of folders exported in environment variables for world writable files/folders.
* WN-FilePermVulns
- Checks the permissions of files/folders related to known vulnerabilities.
* WN-RDSModuleCheck
- Checks if an RDS socket can be opened (blacklisted as a mitigation for CVE-2010-3904)
* WN-Torque
- Checks if torque server has vulnerable options

%prep
%setup -q

%build

%install
export DONT_STRIP=1
%{__rm} -rf %{buildroot}
install --directory %{buildroot}%{dir}

# Install probes for general usage
%{__cp} -rpf .%dir/probes  %{buildroot}%{dir}

# gLite configuration
%{__cp} -rpf .%dir/gLite  %{buildroot}%{dir}
%{__cp} -rpf .%dir/probes  %{buildroot}%{dir}/gLite/wnjob/%{site}/probes/%{site}

# ARC configuration
%{__cp} -rpf .%dir/ARC  %{buildroot}%{dir}
chmod +x %{buildroot}%{dir}/ARC/CE-Jobsubmit
cd .%dir/probes/
tar -zcvf %{buildroot}%{dir}/ARC/jobsubmit/probes.tar.gz *
cd -

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{dir}

%changelog
* Wed Nov 14 2012 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.6-4
- Added dcache-perm probe

* Tue Mar 13 2012 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.6-1
- Fixed Permission blacklisting issues

* Wed Mar 7 2012 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.5-1
- SAM-2465: Add .snapshot to blacklisted directories for Permissions probe
- Updated pakiti-client

* Tue Mar 6 2012 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.4-1
- SAM-2463: Ability to ignore expired CRLs on CRL check

* Tue Mar 6 2012 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.3-1
- SAM-2463: Ability to ignore expired CRLs on CRL check

* Tue Oct 25 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.2-1
- SAM-2106: Fixed typos in Pakiti probe wrapper

* Tue Oct 25 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.1-1
- SAM-2104: Blacklisting directories in Permissions probe
- SAM-2105: Torque probe failing to execute qmgr

* Tue Sep 13 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 1.0.0-1
- SAM-1801: Renamed package to grid-monitoring-probes-eu.egi.sec
- SAM-1895: Added support for ARC sites
- SAM-1910: Added CAs to use for pakiti client/server connections

* Wed Aug 17 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.6-1
- Fixed SAM-1796

* Tue Aug 9 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.5-2
- Updated changelog (and release to force new build)

* Tue Aug 9 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.5-1
- Re-fixed SAM-1727

* Tue Aug 9 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.4-1
- Re-fixed SAM-1760

* Tue Aug 9 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.3-1
- Fixed SAM-1727

* Tue Aug 9 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.2-1
- Fixed SAM-1760

* Wed Feb 9 2011 Emir Imamagic <eimamagi@srce.hr> - 0.3.1-1
- Fixed SAM-1257

* Tue Feb 1 2011 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.3.0-1
- Fixed SAM-1220

* Mon Dec 13 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.2.1-1
- Bug fixes

* Fri Oct 22 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.2.0-1
- Fixed SAM-879

* Mon Aug 16 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.1.7-1
- Fixed SAM-700

* Wed Jul 28 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.1.6-1
- Fixes SAM-675
- Fixes SAM-679

* Wed Jul 28 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.1.5-2
- Changed pakiti server

* Tue Apr 27 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.1.5-1
- Fixes SAM-564
- detailed changelog in CHANGES

* Tue Apr 27 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.1.4-1
- Changed the encryption method
- Added org.sam.sec.WN-CRL probe

* Tue Apr 20 2010 Christos Triantafyllidis <ctria@grid.auth.gr> - 0.1.3-1
- Added ARCH reporting for pakiti

* Mon Jan 25 2010 C. Triantafyllidis <ctria@grid.auth.gr> - 0.1.2-3
- Fixed the _encrypted definition

* Mon Jan 25 2010 C. Triantafyllidis <ctria@grid.auth.gr> - 0.1.2-2
- Added the missing jdl template

* Thu Jan 21 2010 C. Triantafyllidis <ctria@grid.auth.gr> - 0.1.2-1
- Added a fake "OK" to the returned result of check_and_encrypt command

* Wed Jan 20 2010 C. Triantafyllidis <ctria@grid.auth.gr> - 0.1.1-1
- Added the check_and_encrypt command
- Added a detail line to pakiti probe (no useful data yet here, just for testing)
- pakiti probe results are sent encrypted back to the server

* Mon Jul 6 2009 C. Triantafyllidis <ctria@grid.auth.gr> - 0.1.0-1
- Initial build
- Based on CE-probe WN tarball assembly 
  * grid-monitoring-probes-org.sam > 0.1.4-5
- Contains probes:
  * WN-Pakiti
