#!/bin/sh

probes="FilePermVulns Pakiti Permissions RDSModuleCheck Torque"

tar -zxf probes.tar.gz

for probe in $probes; do
  ./${probe} > ${probe}.msg
  echo $? > ${probe}.res
done

exit 0