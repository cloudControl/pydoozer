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
import pydoozer.doozer as doozer
import gevent
from gevent.timeout import Timeout
from pydoozer.jobs.job_manager import JobManager


class DoozerWatchProvider(object):
    """
        The DoozerWatchProvider is basically a wrapper to a given Doozerd
        Cluster, focusing on providing a method to create asynchronous watches
        for objects that can be stored to Doozerd. An external library can
        register callbacks for specified "watch paths". A "watch" is a Doozer
        wait on a provided Doozerd tree path; as soon as a new object is
        written to this path the DoozerProvider will recognize the change and
        start calling the registered callback function.

        All jobs are managed via a Job Manager in a queue. Jobs can easily be
        added, referenced and removed.
    """

    # The doozer client
    client = None

    # the current revision of the client
    revision = None

    # the job manager
    job_queue = JobManager()

    # The doozerd address information, e.g. "doozerd:?ca=10.224.65.94:8046"
    doozerd_server = None

    def __init__(self, doozerd_server):
        """
            Establish a connection to doozerd right upon instantiation
        """
        self.connect(doozerd_server_address=doozerd_server)

    #noinspection PyArgumentList
    def connect(self, doozerd_server_address):
        """
            Connect to a given doozer cluster
        """
        #noinspection PyUnresolvedReferences
        self.client = doozer.connect(doozerd_server_address)
        self.revision = self.client.rev().rev

    def disconnect(self):
        """
            Disconnect from doozer cluster
        """
        self.client.disconnect()

    def _watch(self, watch_path, callback):
        """
            This is the actual watch method. You do not call this directly,
            instead use register_callback and deregister_callback.

            _watch will create an artificial watch (while-True-loop with
            built-in timeout) which will wait for events to happen on a
            given path within the doozerd tree. If nothing happens within
            2 seconds (gevent-defined timeout) the timeout will simply
            update the revision of the client and go back into the
            while-True-loop. If an event is triggered (= a new configuration
            has been received in doozerd) the object will be retrieved and
            the registered callback method from the external caller will be
            triggered, passing in the configurationobject as parameter.
        """
        while True:
            try:
                change = self.client.wait(watch_path, self.revision)
                self.revision = change.rev + 1

                # As soon as something happens, we get following call ...
                configuration_information = self.client.get(watch_path)

                # Ok, call the callback function
                callback(configuration_information)

            except Timeout:
                # Nothing happened because we ran into gevent timeout ...
                self.revision = self.client.rev().rev

                #noinspection PyUnusedLocal
                change = None

    def register_callback(self, watch_path, callback_function):
        """
            This is the actual call for starting a watch. As soon as "watch"
            receives new information the given callback_function is called with
            the configuration information as parameter.

            This method is non-blocking!
        """
        job = gevent.spawn(
            self._watch,
            watch_path=watch_path,
            callback=callback_function
        )
        self.job_queue.add(
            job=job,
            watch_path=watch_path,
            callback_function=callback_function
        )
        return job

    def deregister_callback(self, watch_path):
        """
            Remove a given watch on a watch_path from the job queue.
        """
        job = self.job_queue.remove(watch_path)
        job.reference.kill()
