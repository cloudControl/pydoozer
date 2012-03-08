#!/usr/bin/env python
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
import gevent
from pydoozer.provider.doozer_watch_provider import DoozerWatchProvider

##########################################################################
#
# CONFIGURATION PARAMETERS
#
##########################################################################

# The path to be watched
WATCH_PATH = "/watch"

# The doozerd cluster address (at least, one node within the cluster)
DOOZERD_ADDRESS = "doozerd:?ca=127.0.0.1:8046"

##########################################################################
#
# METHOD DEFINITIONS
#
##########################################################################


def on_config_change(configuration):
    """
        A simple callback function
    """
    print "Received new configuration:"
    print configuration


def main():
    """
        Demo method
    """
    # Connect to doozerd cluster
    doozer_watch_provider = DoozerWatchProvider(doozerd_server=DOOZERD_ADDRESS)

    # Register a watch; provide the callback function that should
    # be called when a new configuration object has been
    # received. This is non-blocking!
    doozer_watch_provider.register_callback(
        watch_path=WATCH_PATH,
        callback_function=on_config_change
    )

    RUN = True
    print ">>> Simply press CTRL-C to quit."
    while RUN:
        try:
            gevent.sleep(10)
            print(">>> Going to sleep for 10 seconds ...")
        except KeyboardInterrupt:
            RUN = False
            print(">>> Aborting run!")

    # Remove the watch from the Doozerd provider
    doozer_watch_provider.deregister_callback(watch_path=WATCH_PATH)


##########################################################################
#
# MAIN
#
##########################################################################

if __name__ == "__main__":
    main()
