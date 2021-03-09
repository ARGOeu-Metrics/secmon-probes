#!/bin/sh

# setup a basic PATH just in case
export PATH=/bin:/usr/bin:/sbin:/usr/sbin:$PATH

tar -zxf WN-probes.tar.gz

for probe in `cat probe_list`; do
  ./WN-probes/${probe} > ${probe}.out 2>&1
  echo $? > ${probe}.res
  sed -i -e '1s/$/|/g' -e "1s/^/$(hostname): /" -e ':a;N;$!ba;s/\n/\\n/g' ${probe}.out
done

exit 0
