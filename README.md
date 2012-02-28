# PyDoozer

A Python client for [Doozer](https://github.com/ha/doozerd) using gevent. This is based on Jeff Lindsay's and
Neuman Vong's [progrium/pydoozer](https://github.com/progrium/pydoozer).

## Status

Still quite early.

## Installation

Install via `pip`:

	$ pip install git+ssh://git@github.com/cloudControl/pydoozer

### Installation error with protobuf 2.4.1 on `python setup.py install`

There is a case when you try to install `pydoozer` via `python setup.py install` and run into following error:

    [..]
    Downloading http://protobuf.googlecode.com/files/protobuf-2.4.1.zip
    Processing protobuf-2.4.1.zip
    error: Couldn't find a setup script in /tmp/easy_install-riZxUs/protobuf-2.4.1.zip

Simply install `protobuf` via `pip` manually:

    $ pip install protobuf

Then run `python setup.py install` again!

Using the `pip install git+ssh://...` method doesn't seem to run into this issue.

For more information check following issue: [Protobuf Issue #66](http://code.google.com/p/protobuf/issues/detail?id=66)

## Todo

 * Entity class to wrap Response objects about entities
 * Finish watch, access support
 * tests, docs
 * Make work with standard python as well as gevent

## Contributors

 * Jeff Lindsay <progrium@twilio.com>
 * Neuman Vong <neuman@twilio.com>
 * Hans-Gunther Schmidt <hgs@cloudcontrol.de>

## License

MIT