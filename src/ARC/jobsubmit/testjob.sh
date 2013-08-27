#!/bin/sh

probes="FilePermVulns Pakiti Permissions RDSModuleCheck Torque check_CVE-2013-2094 check_EGI-SVG-2013-5890"
export SITE_NAME=`cat sitename 2> /dev/null`

tar -zxf probes.tar.gz

for probe in $probes; do
  ./${probe} > ${probe}.msg
  echo $? > ${probe}.res
done

exit 0
