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

"""Creates the Compute Engine."""

NETWORK_NAME = 'a-new-network'
PROJECT_NAME = 'dius-gcp-dev'
DEFAULT_ZONE = 'us-central1-c'

def GenerateConfig(unused_context):
  """Creates the Compute Engine with multiple templates."""
  name='solution'
  region='us-central1'

  resources = [{
      'name': name + '-it',
      'type': 'instance-template-t.py',
      'properties': {
          'project': PROJECT_NAME,
          'machineType': 'f1-micro',
          'zone': DEFAULT_ZONE
      }
  }, {
      'name': name + '-igm',
      'type': 'instance-group-t.py',
      'properties': {
          'zone': DEFAULT_ZONE,
          'size': 8,
          'instance-template': name + '-it',
          'target-pools': name + '-tp',
      }
  }, {
      'name': name + '-as',
      'type': 'compute.v1.autoscaler',
      'properties': {
          'zone': DEFAULT_ZONE,
          'target': '$(ref.' + name + '-igm.selfLink)',
          'autoscalingPolicy': {
              'maxNumReplicas': 8
          }
      }
  }, {
      'name': name + '-hc',
      'type': 'compute.v1.httpHealthCheck',
      'properties': {
          'port': 80,
          'requestPath': '/'
      }
  }, {
      'name': name + '-tp',
      'type': 'compute.v1.targetPool',
      'properties': {
          'region': region,
          'healthChecks': ['$(ref.' + name + '-hc.selfLink)']
      }
  }, {
      'name': name + '-lb',
      'type': 'compute.v1.forwardingRule',
      'properties': {
          'region': region,
          'portRange': 80,
          'target': '$(ref.' + name + '-tp.selfLink)'
     } 
  }]
  return {'resources': resources}
