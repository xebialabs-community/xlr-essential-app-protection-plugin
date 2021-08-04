#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests
import json
import time
from datetime import date, datetime, timedelta
import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Arxan")

def protectWebArtifact(serverParams, fileUrl, fileType, blueprintUrl, seed, product, version):
    agent_url = serverParams.get('url')
    # Install Protect-Web 4.0 on the Agent if it isn't already, and get its ID
    tool_id = installTool(
        agent_url, 
        serverParams.get('key'), 
        serverParams.get('secret'), 
        product, version)
    # Create a protection job
    job_id = requests.post(agent_url+"/api/jobs", json={'tool_id' : tool_id}).json()['job_id']
    # Add our input file(s)
    if fileType == "Archive File":
        addJobFileURL(agent_url, job_id, 'input', "unprotected", fileUrl, unpack_archive='zip')
    else:
        addJobFileURL(agent_url, job_id, 'input', "unprotected", fileUrl)
    # Add the blueprint file
    addJobFileURL(agent_url, job_id, 'blueprint', 'blueprint.json', blueprintUrl)
    # Configure the job
    jobSettings = {
        'licenseToken' : serverParams.get('license'),
        'seed' : seed
    }
    addJobSettings(agent_url, job_id, jobSettings)
    # Run the job
    requests.post(agent_url + "/services/v2/apaas/upload/apps")
    # Wait for the job to finish
    return waitForJobCompletion(agent_url, job_id)

def uploadArtifact(serverParams, fileUrl):
    agent_url = serverParams.get('url')

    # Add our input file(s)
    if fileType == "Archive File":
        addJobFileURL(agent_url, job_id, 'input', "unprotected", fileUrl, unpack_archive='zip')
    else:
        addJobFileURL(agent_url, job_id, 'input', "unprotected", fileUrl)
    # Add the blueprint file
    addJobFileURL(agent_url, job_id, 'blueprint', 'blueprint.json', blueprintUrl)
    # Configure the job
    jobSettings = {
        'licenseToken' : serverParams.get('license'),
        'seed' : seed
    }
    addJobSettings(agent_url, job_id, jobSettings)
    # Run the job
    requests.post(agent_url+"/api/jobs/{}/submit".format(job_id))
    # Wait for the job to finish
    return waitForJobCompletion(agent_url, job_id)

# Tell the agent to install a certain tool
def installTool(agent_url, client_id, client_secret, product, version, timeout=300):
    deadline = datetime.now()+timedelta(seconds=timeout)
    params={'product' : product, 'version' : version}
    # If it's already installed and ready, just grab the ID
    installedTools = requests.get(agent_url+"/api/tools", params=params).json()
    if len(installedTools) == 0:
        logger.error("Installing {0} v{1} on agent server...".format(product, version))
        # Tool is not installed or installing on the agent.  Ask the agent to install it
        requestData = {
            'client_id' : client_id,
            'client_secret' : client_secret,
            'product' : product,
            'version' : version
        }
        r = requests.post(agent_url+"/api/tools", json=requestData)
        tool_id = r.json()['id']
    else:
        # Tool is installed or installing already.  Check the status
        tool = installedTools[0]
        tool_id = tool['id']
        # If it's ready to roll, just return its id
        if tool['status'] == 'ready':
            logger.error("{0} v{1} is already installed on agent server.".format(product, version))
            return tool_id
        # If it's not ready and not installing, cry uncle 
        elif tool['status'] != 'installing':
            raise Exception("Tool is already present, but not installing or ready to use (status = '{}').  Check server and try later.".format(tool['status']))
    # At this point we know the id of our tool and are waiting for it to finish installing
    logger.error("Waiting for tool installation to complete...")
    while datetime.now() < deadline:
        # When status flips to ready, return the tool id to use for jobs
        if requests.get(agent_url+"/api/tools/"+tool_id).json()['status'] == 'ready':
            logger.error("{0} v{1} is installed and ready.".format(product, version))
            return tool_id
        # Chill out and give the installation time to work
        time.sleep(10)
    raise Exception("Timed out waiting for tool installation.")

JOB_FILE_URL = "/api/jobs/{0}/files/{1}/{2}"
# Upload a local file to the specified job under the specified category
def addJobFileURL(agent_url, job_id, category, fileName, fileUrl, unpack_archive=None):
    uploadInfo = {'file_url' : fileUrl}
    if unpack_archive is not None:
        uploadInfo['unpack_archive'] = unpack_archive
    requests.post(agent_url+JOB_FILE_URL.format(job_id, category, fileName), data=uploadInfo)

JOB_SETTINGS_URL = "/api/jobs/{0}"
# Add configuration settings to a job
def addJobSettings(agent_url, job_id, settings):
    requests.put(agent_url+JOB_SETTINGS_URL.format(job_id), json=settings)

# Wait for completion of a specified job on the agent server
def waitForJobCompletion(agent_url, job_id, timeout=300):
    logger.error("Waiting for agent to complete job...")
    deadline = datetime.now() + timedelta(seconds=timeout)
    while datetime.now() < deadline:
        status = requests.get(agent_url+"/api/jobs/"+job_id).json()['status']
        if status in ['completed', 'failed']:
            return status
        time.sleep(10)
    raise Exception("Timed out waiting for job completion")