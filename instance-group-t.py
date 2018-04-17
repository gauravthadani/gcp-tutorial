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
      'type': 'compute.v1.instanceGroupManager',
      'properties': {
	      'zone': context.properties['zone'],
	      'targetSize': context.properties['size'],
	      'targetPools': ['$(ref.' + context.properties['target-pools'] + '.selfLink)'],
          'baseInstanceName': context.env['name'] + '-instance',
          'instanceTemplate': '$(ref.' + context.properties['instance-template'] + '.selfLink)'
      
      }
  }]
  return {'resources': resources}