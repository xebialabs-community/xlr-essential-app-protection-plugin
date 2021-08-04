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
import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Arxan")

# New ARXAN logic
# setup the request url
api_token_endpoint = "/services/oauth2/token"
url = configuration.url + "%s" % api_token_endpoint

# setup the request payload and headers
#payload = "grant_type=client_credentials&client_id=%s" % configuration.key
#payload = payload + "&client_secret=%s" % configuration.secret
headers = {
    'Content-Type': "application/x-www-form-urlencoded"
}
payload = {
    'client_id': configuration.key,
    'client_secret': configuration.secret,
    'grant_type': 'client_credentials'
}

# send post request to services/oauth2/token endpoint
r = requests.post(url, json=payload)
logger.error("TestConnection.py line 30 (after post call)")

# check for good response
if r.status_code != 200:
    raise Exception(
        "Error retrieving authorization token from Arxan Server. Reason: %s" % r.reason
    )
else:
    logger.error('Arxan response token: %s' % r.text)