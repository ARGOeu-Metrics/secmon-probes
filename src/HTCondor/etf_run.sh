#!/bin/bash

# experimental HTCondor security monitoring job

# decompress HTCondor probe payload
tar zxf gridjob.tgz

# source our environment variable(s)
source ./etf-env.sh

# get Worker Node hostname
gatheredAt=`hostname -f`

# CE hostname
service_uri=$eu_egi_sec_service_uri

# run probes
for probe in `cat probe_list`; do
   ./WN-probes/${probe} > ${probe}.out 2>&1
   retv=$?
   case $retv in
     0)
       status="OK"
       ;;
     1)
       status="WARNING"
       ;;
     2)
       status="CRITICAL"
       ;;
     *)
       status="UNKNOWN"
       ;;
   esac

   
   #sed -i -e '1s/$/|/g' -e ':a;N;$!ba;s/\n/\\n/g' ${probe}.out
   sed -i 's/"/\\"/g' ${probe}.out

   summary=$(head -1 ${probe}.out)

   details=$(sed '1d;:a;N;$!ba;s/\n/\\n/g' ${probe}.out)

   printf '{"nagios_name":"%s","service_uri":"%s","status":"%s","summary":"%s","details":"%s","gatheredAt":"%s"}' \
          "eu.egi.sec.WN-${probe}-ops" "$service_uri" "$status" "$summary" "$details" "$gatheredAt" > ${probe}.json
   
done

# gather results in a tarball
tar -zcf wnlogs.tgz *.out *.json

exit 0
