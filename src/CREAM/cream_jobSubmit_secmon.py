#!/usr/bin/env python
"""
Copyright (c) Members of the EGEE Collaboration. 2006-2010.
See http://www.eu-egee.org/partners/ for details on the copyright holders.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

------------------------------------------------------------------------------------------------
Nagios plugin which submits a job to CREAM CE, checks its terminal status and finally purges it. 
------------------------------------------------------------------------------------------------
"""
__author__ = "Lisa Zangrando lisa.zangrando@pd.infn.it"
__date__ = "31.05.2018"
__version__ = "0.1.0"

import time
import dircache
import shutil
import os
from cream import Client

nagcmd = "/var/nagios/rw/nagios.cmd"

def main():
    client = Client("cream-jobSubmit", "1.0")
    client.createParser()
    client.optionParser.add_option("-m",
                         "--metrics",
                         dest="metrics_list",
                         help="The metrics file path")
    client.readOptions()

    if not client.options.metrics_list:
        optionParser.error("metrics file path not specified")

    try:
        with open(client.options.metrics_list) as infile:
            data = infile.read()

        metrics = data.splitlines()
    except Exception as ex:
        client.nagiosExit(client.CRITICAL, ex)
 
    try:
        client.checkProxy()

        jobId = client.jobSubmit()

        client.debug("job id: " + jobId)
    except Exception as ex:
        client.nagiosExit(client.CRITICAL, ex)

    terminalStates = ['DONE-OK', 'DONE-FAILED', 'ABORTED', 'CANCELLED']
    lastStatus = ""
    exitCode = None

    while not lastStatus in terminalStates:
        time.sleep(10)
        try:
            lastStatus, exitCode = client.jobStatus(jobId)

            client.debug("job status: " + lastStatus)
        except Exception as ex:
            client.nagiosExit(client.CRITICAL, ex)

    try:
        client.dir = "/var/spool/cream/" + client.hostname
        if not os.path.isdir(client.dir):
            os.makedirs(client.dir)

        osbdir = client.getOutputSandbox(jobId)

        client.debug("output sandbox dir: " + osbdir)

        outfiles = dircache.listdir(osbdir)

    except Exception as ex:
        client.nagiosExit(client.CRITICAL, ex)

    for metric in metrics:
        client.debug("metric is " + metric)
        outfilename = osbdir + "/" + metric + ".out"
        resfilename = osbdir + "/" + metric + ".res"
        client.debug("outfile is " + outfilename)
        client.debug("resfile is " + resfilename)
        if os.path.isfile(outfilename) and os.path.isfile(resfilename) :
            with open(outfilename) as outfile:
                data = outfile.read()
            output = data.splitlines()

            outmsg = ""
            sep = "\\\\n"
            for line in output:
                outmsg += line + "\\\\n"

            with open(resfilename) as resfile:
                data = resfile.read()
            exitvalue = data.splitlines()

            currtime = str(int(time.mktime(time.localtime())))
            
            nagmsg = "[" + currtime + "] PROCESS_SERVICE_CHECK_RESULT;" + client.hostname + \
                  ";eu.egi.sec.WN-" + metric + "-ops;" + exitvalue[0] + ";" + outmsg + '\n'
            client.debug("Results submitted to nagios: " + nagmsg)
            with open(nagcmd, 'a') as nagcmdfile:
                  nagcmdfile.write(nagmsg)

        else:
            currtime = str(int(time.mktime(time.localtime())))
            nagmsg = "[" + currtime + "] PROCESS_SERVICE_CHECK_RESULT;" + client.hostname + \
                  ";eu.egi.sec.WN-" + metric + "-ops;" + "3;(No output returned from plugin)" + '\n'
            client.debug("Results submitted to nagios: " + nagmsg)
            with open(nagcmd, 'a') as nagcmdfile:
                  nagcmdfile.write(nagmsg)

    try:       
        client.jobPurge(jobId)
    except Exception as ex:
        client.debug("cannot purge the job" + ex)

    if lastStatus == terminalStates[0] :
        client.nagiosExit(client.OK, "Job terminated with status=" + lastStatus)
    else:
        client.nagiosExit(client.CRITICAL, "Job terminated with status=" + lastStatus)



if __name__ == '__main__':
    main()

