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
from pydoozer.jobs.Job import Job
from pydoozer.jobs.job_manager import JobManager


class JobManagerTests(unittest.TestCase):

    # a single job
    job = None

    # job queue
    queue = None

    # A fake object that will be put into a job as "job" reference
    fake_gevent_background_process = "background_process"

    # watch paths
    watch_path_1 = "/watch1"
    watch_path_2 = "/watch2"
    watch_path_3 = "/watch3"

    # A fake callback function
    def on_configuration_change(self, configuration):
        print "Configuration change:"
        print configuration

    def setUp(self):
        super(JobManagerTests, self).setUp()
        self.queue = JobManager()
        self.job = Job(
            job=self.fake_gevent_background_process,
            watch_path=self.watch_path_1,
            callback_function=self.on_configuration_change
        )

    def tearDown(self):
        super(JobManagerTests, self).tearDown()
        self.job = None
        self.queue = None

    def test_add_job(self):
        self.assertEqual(self.queue.size(), 0)
        self.queue.add(
            self.job,
            watch_path=self.watch_path_1,
            callback_function=self.on_configuration_change
        )
        self.assertEqual(self.queue.size(), 1)

    def test_add_same_job_twice_fails(self):
        self.queue.add(
            self.job,
            watch_path=self.watch_path_1,
            callback_function=self.on_configuration_change
        )
        self.queue.add(
            self.job,
            watch_path=self.watch_path_1,
            callback_function=self.on_configuration_change
        )
        self.assertEqual(self.queue.size(), 1)

    def test_add_multiple_jobs(self):
        self.queue.add(
            self.job,
            watch_path=self.watch_path_1,
            callback_function=self.on_configuration_change
        )
        self.queue.add(
            self.job,
            watch_path=self.watch_path_2,
            callback_function=self.on_configuration_change
        )
        self.queue.add(
            self.job,
            watch_path=self.watch_path_3,
            callback_function=self.on_configuration_change
        )
        self.assertEqual(self.queue.size(), 3)

    def test_remove_single_job(self):
        self.queue.add(
            self.job,
            watch_path=self.watch_path_1,
            callback_function=self.on_configuration_change
        )
        self.queue.add(
            self.job,
            watch_path=self.watch_path_2,
            callback_function=self.on_configuration_change
        )
        self.assertEqual(self.queue.size(), 2)

        self.queue.remove(self.watch_path_2)
        self.assertEqual(self.queue.size(), 1)

        self.queue.remove(self.watch_path_1)
        self.assertEqual(self.queue.size(), 0)


####################################################################
#
# MAIN
#
####################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JobManagerTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
