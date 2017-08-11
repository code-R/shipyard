# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import falcon
from falcon import testing
import mock

from shipyard_airflow.control import api
from shipyard_airflow.control.airflow_connections import AirflowAddConnectionResource


class AirflowAddConnectionResourceTestCase(testing.TestCase):
    def setUp(self):
        super(AirflowAddConnectionResourceTestCase, self).setUp()
        self.app = api.start_api()

    def test_on_get_500(self):
        doc = {
            'title': 'Internal Server Error',
            'description': 'Missing Configuration File'
        }
        result = self.simulate_get(
            '/api/v1.0/connections/add2/conn_id/1/protocol/protocol/host/host/port/2',
            headers={'X-Auth-Token': '10'})
        assert result.json == doc
        assert result.status == falcon.HTTP_500

    @mock.patch.object(AirflowAddConnectionResource, 'retrieve_config')
    def test_on_get_400(self, mock_config):
        doc = {
            'type': 'error',
            'message': 'Invalid Paremeters for Adding Airflow Connection',
            'retry': False
        }
        mock_config.return_value = 'some_url'
        result = self.simulate_get(
            '/api/v1.0/connections/add2/conn_id/1/protocol/protocol/host/host/port/2',
            headers={'X-Auth-Token': '10'})
        assert result.json == doc
        assert result.status == falcon.HTTP_400
