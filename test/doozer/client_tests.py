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
from doozer.client import parse_uri, connect, ConnectError


class ClientTests(unittest.TestCase):
    def setUp(self):
        super(ClientTests, self).setUp()


    def tearDown(self):
        super(ClientTests, self).tearDown()


    def test_parse_uri(self):
        # These URIs should all raise exceptions!
        self.assertRaises(ValueError, parse_uri, "1.2.3.4")
        self.assertRaises(ValueError, parse_uri, "300.300.300.300")
        self.assertRaises(ValueError, parse_uri, "1.2.3.4:8046")
        self.assertRaises(ValueError, parse_uri, "doozer:?ca=1.2.3.4:8046")

        # This URI should work!
        self.assertEqual(['1.2.3.4:8046'], parse_uri(uri="doozerd:?ca=1.2.3.4:8046"))


    def test_connect(self):
        # connect() should raise an exception IF YOU DON'T have a local doozer cluster running
        self.assertRaises(ValueError, connect, "1.2.3.4:8046")
        self.assertRaises(ConnectError, connect, "doozerd:?ca=1.2.3.4:8046")

####################################################################
#
# MAIN
#
####################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClientTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
