# -*- coding: utf-8 -*-
"""
    Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

"""
import unittest
from mock import Mock
from mock import patch


from pydoozer.doozer.client import connect
from pydoozer.doozer.client import parse_uri
from pydoozer.doozer.client import ConnectError
from pydoozer.doozer.client import CONNECT_TIMEOUT
from pydoozer.doozer.client import MAX_RECONNECT_RETRIES


class ClientTests(unittest.TestCase):

    def setUp(self):
        super(ClientTests, self).setUp()

    def test_parse_uri(self):
        # These URIs should all raise exceptions!
        self.assertRaises(ValueError, parse_uri, "1.2.3.4")
        self.assertRaises(ValueError, parse_uri, "300.300.300.300")
        self.assertRaises(ValueError, parse_uri, "1.2.3.4:8046")
        self.assertRaises(ValueError, parse_uri, "doozer:?ca=1.2.3.4:8046")

        # This URI should work!
        self.assertEqual(['1.2.3.4:8046'], parse_uri(uri="doozerd:?ca=1.2.3.4:8046"))

    def test_connect_error(self):
        # connect() should raise an exception IF YOU DON'T have a local doozer cluster running
        self.assertRaises(ValueError, connect, "1.2.3.4:8046", timeout=0.1, reconnect_retries=1)
        self.assertRaises(ConnectError, connect, "doozerd:?ca=1.2.3.4:8046", timeout=0.1, reconnect_retries=1)

    @patch('pydoozer.doozer.client.Connection')
    def test_connect_success(self, class_connection):
        # connect() should return a client object
        connection = Mock()
        class_connection.return_value = connection
        client = connect("doozerd:?ca=127.0.0.2:8046")
        
        self.assertEqual(['127.0.0.2:8046'], class_connection.call_args[0][0])
        self.assertEqual(CONNECT_TIMEOUT, connection.connect.call_args[0][0])
        self.assertEqual(MAX_RECONNECT_RETRIES, connection.connect.call_args[0][1])
        self.assertEqual(connection, client.connection)



####################################################################
#
# MAIN
#
####################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClientTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
