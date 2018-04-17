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


def startup_script():
  return """
    sudo apt-get install -y nginx
    sudo curl -fsSL get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo docker run -d -p 8080:8080 gauravthadani/istiosample
    sudo echo " server {
          listen 80;
          server_name ~^.*$;
          location / {
              proxy_pass http://127.0.0.1:8080/hello;
           }
    }" >> /etc/nginx/conf.d/myapp.conf
    sudo systemctl restart nginx

  """

def GenerateConfig(context):
  """Creates the instance group template with environment variable."""
  
  default_network = ''.join(['https://www.googleapis.com/compute/v1/projects/',
                             context.env['project'],
                             '/global/networks/default'])

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
              'network': default_network,
              'accessConfigs': [{
                  'name': 'External NAT',
                  'type': 'ONE_TO_ONE_NAT'
              }]
          }],
          'metadata': {
              'items': [{
                  'key': 'startup-script',
                  'value': startup_script(),
              }]
          }
      }
    }
  }]

  outputs = [{'name': 'instanceTemplateSelfLink',
              'value': '$(ref.' + context.env['name'] + '.selfLink)'}]

  return {'resources': resources, 'outputs': outputs}