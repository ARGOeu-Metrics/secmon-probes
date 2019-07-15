# secmon-probes

The security monitoring probes consist of active and passive checks. The active checks are executed on the Nagios server. The passive checks are executed on the
Worker Nodes via a grid job that is submitted to each CREAM CE and ARC CE.

* Active checks:
  * check_pakiti_vuln
  * argus-ban

* Passive checks:
  * CRL
  * FilePermVulns
  * Pakiti
  * Permissions
  * RDSModuleCheck
  * Torque
  * check_CVE-2013-2094
  * check_CVE-2015-3245
  * check_CVE-2016-5195
  * check_EGI-SVG-2016-5195
  * check_EGI-SVG-2018-14213
  * check_CVE-2018-1111
  * check_CVE-2018-12021
  * check_CVE-2018-14634
  * dcache-perms
  * libkeyutils

## ARC CE tests

For the ARC CE job submission we use the [http://git.nbi.ku.dk/downloads/NorduGridARCNagiosPlugins/arcce.html NorduGrid ARC Nagios Plugins].

## CREAM CE tests

For the CREAM CE job submission we use a script heavily based on the [https://wiki.italiangrid.it/twiki/bin/view/CREAM/DjsCreamProbeNew Italiangrid CREAM-CE direct job submission metrics]. Our version of """cream_jobSubmit.py""" is modified so it submits a job payload containing all the security passive checks, it retrieves the output and posts the results to Nagios.

## Directory structure

* `src/arc`: ARC Nagios Plugins configuration file
* `src/CREAM`: CREAM direct job submissions files
* `src/WN-probes`: Passive checks
* `src/probe-src`: Source code of RDSModuleCheck
* `src/probes` : Active checks

