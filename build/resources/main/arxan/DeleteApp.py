#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import requests
import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Arxan")

# New ARXAN logic
# setup the request url
api_token_endpoint = "/v2/apaas/apps/%s" % protection_id
url = server.get('url') + "%s" % api_token_endpoint
logger.info('Deleting app from the server...')
headers = {
    'Authorization': auth_string,
}

response = requests.delete(url, headers=headers, verify=False)
output = response.json()

if response.status_code == 200:
    logger.debug('Deleting app from the server response: %s', response.json())
    logger.info('App deleted from the server')
elif response.status_code == 404:
    logger.error("App doesn't exist.")
elif response.status_code == 401 or response.status_code == 403:
    raise AuthorizationError()
else:
    logger.error("An unexpected error has occurred.")
    raise Exception('Incorrect response code for delete app: (%s)', response.status_code)