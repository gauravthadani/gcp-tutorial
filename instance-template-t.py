# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Creates the instance group template."""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
  """Creates the instance group template with environment variable."""
  resources = [{
      'name': context.env['name'],
      'type': 'compute.v1.instanceTemplate',
      'properties': {
        'project': context.properties['project'],
        'properties': {
          'machineType': context.properties['machineType'],
          'disks': [{
              'deviceName': 'boot',
              'type': 'PERSISTENT',
              'boot': True,
              'autoDelete': True,
              'initializeParams': {
                  'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/',
                                          'debian-cloud/global/',
                                          'images/family/debian-8'])
              }
          }],
          'networkInterfaces': [{
              'network': '$(ref.' + context.properties['network'] + '.selfLink)',
              'accessConfigs': [{
                  'name': 'External NAT',
                  'type': 'ONE_TO_ONE_NAT'
              }]
          }],
          'metadata': {
              'items': [{
                  'key': 'startup-script',
                  'value': ''.join(['#!/bin/bash\n',
                                    'sudo apt-get update\n',
'sudo apt-get install -y nginx\n',
'sudo curl -fsSL get.docker.com -o get-docker.sh\n',
'sudo sh get-docker.sh\n',
'sudo docker run -d -p 8080:8080 gauravthadani/istiosample\n',
'sudo echo " server {\n',
'\n',
        'listen 80;\n',
        'server_name ~^.*$;\n',
         'location / {\n',
        'proxy_pass http://127.0.0.1:8080/hello;\n',
        '}\n',
'}" >> /etc/nginx/conf.d/myapp.conf\n',
'sudo systemctl restart nginx\n'])
              }]
          }
      }
    }
  }]
  return {'resources': resources}