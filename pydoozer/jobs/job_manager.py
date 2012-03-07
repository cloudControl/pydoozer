# -*- coding: utf-8 -*-
"""
    Copyright (c) 2012 cloudControl GmbH

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

"""
from pydoozer.jobs.Job import Job


class JobManager(object):
    """
        The Job Manager manages single jobs in a queue. Jobs can be added,
        searched and removed.
    """

    # Job queue
    jobs = []

    def __init__(self):
        self.jobs = []

    def add(self, job, watch_path, callback_function):
        """
            Add a new job with given watch path and registered callback
            function into the job queue. If a job already exists on the
            given watch path, this job is handed back.
        """
        old_job = self.get(watch_path)
        if old_job:
            return old_job

        new_job = Job(
            job=job,
            watch_path=watch_path,
            callback_function=callback_function
        )
        self.jobs.append(new_job)
        return new_job

    def get(self, watch_path):
        """
            Find the job within the job queue that matches the watch_path.
        """
        for job in self.jobs:
            if watch_path == job.watch_path:
                return job

    def remove(self, watch_path):
        job_to_remove = self.get(watch_path)
        self.jobs.remove(job_to_remove)
        return job_to_remove

    def size(self):
        """
            Size of the job queue (number of jobs managed in the queue)
        """
        return len(self.jobs)
