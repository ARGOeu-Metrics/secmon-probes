# secmon-probes

The security monitoring probes consist of active and passive checks. The active checks are executed on the Nagios server. The passive checks are executed on the
Worker Nodes via a grid job that is submitted to each ARC CE, CREAM CE and HTCondor-CE.

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
  * check_CVE-2019-12528
  * check_CVE-2021-3156
  * check_CVE-2021-4034
  * check_CVE-2022-25235
  * check_CVE-2022-25236
  * check_CVE-2022-2588
  * check_CVE-2022-40674
  * check_CVE-2023-32233
  * check_CVE-2024-1086
  * dcache-perms
  * libkeyutils

## ARC CE tests

For the ARC CE job submission we use the [NorduGrid ARC Nagios Plugins](http://git.nbi.ku.dk/downloads/NorduGridARCNagiosPlugins/arcce.html).

## CREAM CE tests

For the CREAM CE job submission we use a script heavily based on the [Italiangrid CREAM-CE direct job submission metrics](https://wiki.italiangrid.it/twiki/bin/view/CREAM/DjsCreamProbeNew). Our version of `cream_jobSubmit.py` is modified so it submits a job payload containing all the security passive checks, it retrieves the output and posts the results to Nagios.

## HTCondor-CE tests

We use the [jess grid job submission library](https://gitlab.cern.ch/etf/jess/) to submit a test job and retrieve the results. The etf_run.sh script, that is submitted with the job payload, executes the passive checks and stores their results in JSON files. The jess library retrieves the job output, reads the JSON files and posts the results to Nagios.

## Directory structure

* `src/arc`: ARC Nagios Plugins configuration file
* `src/CREAM`: CREAM direct job submissions files
* `src/HTCondor`: HTCondor-CE payload executable script and probe list
* `src/WN-probes`: Passive checks
* `src/probe-src`: Source code of RDSModuleCheck
* `src/probes` : Active checks

