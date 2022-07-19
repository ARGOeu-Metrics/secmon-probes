%define site eu.egi.sec
%define ourdir %{_libexecdir}/grid-monitoring/probes/%{site}

%define debug_package %{nil}

Summary: Security monitoring probes based on EGI CSIRT requirements
Name: grid-monitoring-probes-eu.egi.sec
Version: 2.1.15
Release: 0%{?dist}

License: ASL 2.0
Group: Applications/System
Source0: %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: emi-cream-nagios
Requires: nordugrid-arc-client
Requires: perl-Text-CSV
Requires: python-jess
Requires: python-suds
AutoReqProv: no
BuildArch: noarch

%description
This package includes the framework to submit grid jobs to monitor the security of the EGI sites.

Currently it supports the following middlewares:
- UMD (CREAM)
- ARC
- HTCondor-CE

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
* WN-dcache-perms
- Check for vulnerable permissions in dcache related folders.
* WN-libkeyutils
- check for any hosts that have a file matching the glob
pattern libkeyutils.so* that doesn't belong to an installed RPM package
* WN-check_CVE-2013-2094 
- check for hosts with old vulnerable kernels
* Pakiti-Check 
- Query pakiti portal and checks if a WN is in the vulnerable list
* WN-check_CVE-2015-3245 
- Check if mitigation for CVE-2015-3245 has been applied
* WN-check_CVE-2016-5195
- Check if mitigation for CVE-2016-5195 has been applied
* WN-check_EGI-SVG-2016-5195
- Check if mitigation for EGI-SVG-2016-5195 has been applied
* WN-check_EGI-SVG-2018-14213
- Check if mitigations for EGI-SVG-2018-14213 have been applied
* WN-check_CVE-2018-1111
- Check if mitigations for CVE-2018-1111 have been applied
* WN-check_CVE-2018-12021
- Check if mitigations for CVE-2018-12021 have been applied
* WN-check_CVE-2018-14634
- Check if mitigations for CVE-2018-14634 have been applied
* WN-check_CVE-2021-3156
- Check if mitigation for CVE-2021-3156 has been applied
* WN-check_CVE-2021-3156
- Check if mitigation for CVE-2021-4034 has been applied
%prep
%setup -q

%build

%install
export DONT_STRIP=1
%{__rm} -rf %{buildroot}
install --directory %{buildroot}%{ourdir}
install --directory %{buildroot}%{_sysconfdir}/arc/nagios
install --directory %{buildroot}/var/spool/cream
install --directory %{buildroot}/var/spool/htcondor

# create this empty dir otherwise check_js is failing
install --directory %{buildroot}/usr/libexec/grid-monitoring/wnfm


# ARC configuration
%{__cp} -rpf .%{_sysconfdir}/arc/nagios/50-secmon.ini %{buildroot}%{_sysconfdir}/arc/nagios
%{__cp} -rpf .%{ourdir}/WN-probes %{buildroot}%{_sysconfdir}/arc/nagios/50-secmon.d
%{__rm} -rf %{buildroot}%{_sysconfdir}/arc/nagios/50-secmon.d/pakiti_cas
cd .%{ourdir}/WN-probes
tar -zcvf %{buildroot}%{_sysconfdir}/arc/nagios/50-secmon.d/pakiti_cas.tar.gz pakiti_cas/
cd -

# CREAM configuration
%{__cp} -rpf .%{ourdir}/CREAM  %{buildroot}%{ourdir}
chmod +x %{buildroot}%{ourdir}/CREAM/cream_jobSubmit_secmon.py
cd .%{ourdir}/
tar -zcvf %{buildroot}%{ourdir}/CREAM/WN-probes.tar.gz WN-probes/
cd -

# HTCondor configuration
%{__cp} -rpf .%{ourdir}/HTCondor  %{buildroot}%{ourdir}
%{__cp} -rpf .%{ourdir}/WN-probes %{buildroot}%{ourdir}/HTCondor

# Install probes for general usage
%{__cp} -rpf .%{ourdir}/probes  %{buildroot}%{ourdir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%ourdir
%{_sysconfdir}/arc/nagios
%attr(755,nagios,nagios) /var/spool/cream
%attr(755,nagios,nagios) /var/spool/htcondor
/usr/libexec/grid-monitoring/wnfm

%changelog
* Tue Jul 19 2022 Baptiste Grenier <baptiste@bapt.name> - 2.1.15-0
- Fixed typos in Permissions probe.

* Wed May 4 2022 Daniel Kouril <kouril@ics.muni.cz> - 2.1.14-0
- Fixed small code irregularities in Permissions probe.

* Wed Apr 27 2022 Jakub Havrila <havrila@cesnet.cz> - 2.1.13-0
- Added a check for CVE-2022-25236.

* Mon Apr 25 2022 Jakub Havrila <havrila@cesnet.cz> - 2.1.12-0
- Added a check for CVE-2022-25235.

* Fri Feb 11 2022 Jakub Havrila <havrila@cesnet.cz> - 2.1.11-0
- check_pakiti_vuln: Changed reader of pakiti API because of new format.

* Thu Feb 03 2022 Daniel Kouril <kouril@ics.muni.cz> - 2.1.10-0
- Added mitigation check for CVE-2021-4034

* Tue Oct 26 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.1.9-0
- Make the Torque probe really exit when qmgr isn't found.

* Mon Oct 25 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.1.8-0
- Updated pakiti server hostname.

* Mon Sep 13 2021 Jakub Havrila <havrila@cesnet.cz> - 2.1.7-0
- Removed old and not working pakiti servers.

* Mon Aug 16 2021 Jakub Havrila <havrila@cesnet.cz> - 2.1.6-0
- Replaced pakiti server pakiti.metacentrum.cz with pakiti.egi.eu.

* Fri Jul 16 2021 Jakub Havrila <havrila@cesnet.cz> - 2.1.5-0
- Added new instance of pakiti server pakiti.metacentrum.cz

* Mon Apr 26 2021 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.1.4-0
- Added python-suds requirement in SPEC file.
- Argus-ban ssl context fix.
- Setup a basic $PATH environment variable for ARC tests.

* Tue Mar 9 2021 Daniel Kouril <kouril@ics.muni.cz> and Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.1.3-0
- check_CVE-2015-3245: Mitigation checks are skipped when the vulnerability isn't present.
- HTCondor-CE etf_run.sh script:
  * Set $SITE_NAME environment variable.
  * Escape backslashes in the output of WN probes.

* Tue Mar 9 2021 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.1.2-0
- Setup a basic $PATH environment variable before executing probes on CREAM and HTCondor-CE.

* Mon Mar 8 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.1.1-0
- check_CVE-2018-12021: Check singularity is available before it's checked.
- CRL: Don't check CRLs if there's no certificate on the system.
- check_CVE-2013-2094,check_CVE-2016-5195,check_CVE-2018-1111,check_CVE-2018-12021,check_CVE-2018-14634,check_CVE-2021-3156,check_EGI-SVG-2016-5195,check_EGI-SVG-2018-14213: Mitigation checks are skipped when the vulnerability isn't present.

* Mon Mar 8 2021 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.1.0-0
- Added support for HTCondor-CE, using the jess grid job submission library.

* Sat Mar 6 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-13
- pakiti-client: Simplify the processing of Pakiti output.

* Tue Mar 2 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-12
- check_CVE-2018-1111: Check properly Pakiti results.

* Wed Feb 24 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-11
- check_CVE-2018-1111: Fix the test of exit status.

* Mon Feb 22 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-10
- pakiti-client: Fix Pakiti reporting using openssl and review processing results from Pakiti
- check_CVE-2018-1111: Check Pakiti results before checking for mitigations

* Sun Feb 14 2021 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-9
- check_CVE-2021-3156: Check if mitigation for CVE-2021-3156 has been applied

* Thu Oct 24 2019 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-8
- check_pakiti_vuln: Only ask for recent machines from Pakiti [ggus #143718]

* Wed Oct 09 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.0.0-7
- check_pakiti_vuln: fix typos
- CREAM: Retrieve also std.out and std.err for debugging purposes

* Fri Sep 27 2019 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-6
- check_pakiti_vuln: update query URL to Pakiti3 server

* Mon Sep 23 2019 Daniel Kouril <kouril@ics.muni.cz> - 2.0.0-5
- Update Pakiti servers

* Wed Mar 6 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.0.0-4
- Fix bug in Permissions test
- Include CRL and dcache-perms in ARC tests

* Tue Feb 19 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.0.0-3
- Add requirement for perl-Text-CSV in SPEC file.
- Create /var/spool/cream.

* Tue Feb 5 2019 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.0.0-2
- Fix CREAM probes packaging bug in SPEC file.
- Use Net::SSL in check_pakiti_vuln, otherwise authentication with Pakiti server fails.

* Tue Nov 27 2018 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 2.0.0-1
- New version, for use with ARGO and Centos 6 or 7.
  The security probes remain the same, but the submission to the sites
  is done using:
  * NorduGrid ARC Nagios Plugins
  * Modified CREAM-CE direct job submission metrics

* Mon Oct 29 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-51
- Use the right operator in check_CVE-2018-14634

* Mon Oct 22 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-50
- check_CVE-2018-14634: add a mitigation check for CVE-2018-14634

* Mon Aug 06 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-49
- check_CVE-2018-12021: add a mitigation test for CVE-2018-12021

* Tue Jun 12 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-48
- check_CVE-2018-1111 : add a mitigation check for CVE-2018-1111

* Thu May 3 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-47
- check_EGI-SVG-2018-14213 : disabling overlay doesn't actually prevent
  from the vulnerability

* Wed May 2 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-46
- check_EGI-SVG-2018-14213 : check all suid commands used by Singularity

* Fri Apr 6 2018 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-45
- Add a check of mitigations for EGI-SVG-2018-14213

* Mon Feb 5 2018 Vincent Brillault - 1.0.11-44
- Argus-ban: don't fail for authorization when listing PAPs

* Tue May 30 2017 Daniel Kouril <kouril@ics.muni.cz> - 1.0.11-43
- Added configuration for a new Pakiti server

* Mon Dec 05 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 1.0.11-42
- Added ARGUS probe

* Tue Nov 22 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 1.0.11-41
- CVE-2016-5195, EGI-SVG-2016-5195: Added detection of a generic stap module

* Mon Oct 24 2016 Kyriakos Gkinis <kyrginis@admin.grnet.gr> - 1.0.11-40
- Removed probe eu.egi.sec.WN-check_EGI-SVG-2013-5890-ops from ARC and CREAM tests
- Added probes for CVE-2016-5195, EGI-SVG-2016-5195

* Tue Jul 05 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-39
- ARC wrapper: Remove dependencies to org.ndgf

* Fri Jun 10 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-38
- ARC wrapper: handle finished state as terminal
- ARC wrapper: added job ids in output messages
- ARC wrapper: added job log in output messages

* Fri Jun 10 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-37
- ARC wrapper: More changes to output handling in ARC script
- ARC wrapper: Reduce time limit for jobs in Q state

* Wed Jun 08 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-36
- More changes to output handling in ARC script

* Wed Jun 08 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-35
- Some more fixes in ARC submit script

* Wed Jun 08 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-34
- Remove redundant line

* Wed Jun 08 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-33
- Improve output messages in case of ARC submission errors

* Wed Jun 01 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-32
- Modified ARC-CE submission script to exit in case of job failure

* Wed Jun 01 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-31
- Removed unused commands from ARC-CE submission script

* Thu Mar 10 2016 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-30
- Update ARC-CE submission script to use the new arc client commands

* Mon Nov 02 2015 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-29
- Add "hostname" of the node on the output of check_pakiti_vuln probe

* Tue Oct 27 2015 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-28
- Fixes false positives with Pakiti for ARC CEs [ggus #115901]

* Tue Sep 22 2015 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-27
- Fixes false positives with Pakiti [ggus #115901]

* Tue Aug 04 2015 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-26
- Added check for CVE-2015-3245

* Mon May 18 2015 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-25
- Fixed bug in Pakiti-check vulnerabilities probe

* Mon Oct 06 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-24
- Updated pakiti servers in pakiti-client

* Tue Sep 16 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-23
- Added quotes into if statements (check_CVE-2013-2094)

* Tue Sep 16 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-22
- Modified probe check_CVE-2013-2094 to ensure that it not returns faulse positives

* Mon Aug 04 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-20
- Modified probe check_CVE-2013-2094 to only check for mitigations

* Thu Jun 26 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-19
- Modified Pakiti-Check to not use nagios epn

* Thu Jun 26 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-18
- Added Pakiti-Check probe as active check

* Thu Jun 26 2014 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-17
- Added Pakiti-Check probe

* Wed Sep 25 2013 George Fergadis <fergadis@grid.auth.gr> - 1.0.11-16
- Fixed Torque probe

* Wed Sep 25 2013 George Fergadis <fergadis@grid.auth.gr> - 1.0.11-15
- Fixed ARC testjob script to report the probe return code

* Tue Sep 24 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-14
- Modified the ARC testjob script to return the hostname of the tested node

* Fri Sep 13 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-13
- check_CVE-2013-2094 version 0.6.

* Fri Aug 30 2013 George Fergadis <fergadis@grid.auth.gr> - 1.0.11-12
- check_EGI-SVG-2013-5890 version 1.5.

* Fri Aug 30 2013 George Fergadis <fergadis@grid.auth.gr> - 1.0.11-11
- check_EGI-SVG-2013-5890 version 1.4.

* Fri Aug 30 2013 George Fergadis <fergadis@grid.auth.gr> - 1.0.11-10
- check_EGI-SVG-2013-5890 version 1.3.

* Fri Aug 30 2013 George Fergadis <fergadis@grid.auth.gr> - 1.0.11-9
- check_EGI-SVG-2013-5890 version 1.2.

* Fri Aug 30 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-8
- check_EGI-SVG-2013-5890 version 1.1.

* Fri Aug 30 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-7
- check_EGI-SVG-2013-5890 version 1.0. Several code improvements.

* Thu Aug 29 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-6
- check_EGI-SVG-2013-5890 version 0.7

* Thu Aug 29 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-5
- check_EGI-SVG-2013-5890 version 0.6

* Thu Aug 29 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-4
- check_EGI-SVG-2013-5890 version 0.5 . Display the hostname too when result is critical.

* Wed Aug 28 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-3
- check_EGI-SVG-2013-5890 version 0.4 .

* Tue Aug 27 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-2
- check_EGI-SVG-2013-5890 version 0.2 . Also some fixes in changelog. 

* Tue Aug 27 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.11-1
- check_EGI-SVG-2013-5890 added 

* Fri Jul 05 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-8
- increased memory limit for ARC probes 

* Thu Jun 06 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-7
- check_CVE-2013-2094 probe was not added into the ARC testjob 

* Thu Jun 06 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-6
- Added support for ARC sites for check_CVE-2013-2094 probe

* Thu May 30 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-5
- Small improvement in WN-CVE-2013-2094 probe at kernel check condition in order to correctly identify xen kernels too

* Tue May 28 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-4
- This is a test build

* Mon May 27 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-3
- Small correction on critical message output in WN-CVE-2013-2094 probe

* Wed May 22 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-2
- Added WN-CVE-2013-2094 probe in gLite services.cfg

* Wed May 22 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.10-1
- Added WN-CVE-2013-2094 probe

* Tue Feb 26 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.9-4
- Fixed changelog date.

* Tue Feb 26 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.9-3
- Defined service libkeyutils in gLite services.cfg

* Mon Feb 25 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.9-2
- Added the code..

* Mon Feb 25 2013 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.9-1
- Added libkeyutils probe

* Thu Feb 14 2013 Anastasis Andronidis <andronat@grid.auth.gr> - 1.0.8-2
- Added dependency on emi-cream-nagios

* Fri Nov 23 2012 Paschalis Korosoglou <pkoro@grid.auth.gr> - 1.0.8-1
- Removed dependency on org.sam

* Mon Nov 19 2012 Pavlos Daoglou <pdaog@grid.auth.gr> - 1.0.7-1
- Fixed issue about dcache-perms failing to be scheduled.
- Fixed, wrong version number.

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

