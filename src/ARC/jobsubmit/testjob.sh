#!/bin/sh

probes="FilePermVulns Pakiti Permissions RDSModuleCheck Torque check_CVE-2013-2094 check_CVE-2015-3245 check_CVE-2016-5195 check_EGI-SVG-2016-5195 check_EGI-SVG-2018-14213"
export SITE_NAME=`cat sitename 2> /dev/null`

tar -zxf probes.tar.gz

for probe in $probes; do
  ./${probe} > ${probe}.msg
  echo $? > ${probe}.res
  sed -i -e "1 s/^/$(hostname): /" ${probe}.msg
done

exit 0
