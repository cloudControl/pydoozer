import os
import sys
sys.path.append(os.path.dirname(__file__) + "/..")

from pydoozer import doozer

client = doozer.connect()

rev = client.set("/foo", "test", 0).rev
print "Setting /foo to test with rev %s" % rev

foo = client.get("/foo")
print "Got /foo with %s" % foo.value

root = client.getdir("/")
print "Directly under / is %s" % ', '.join([f.path for f in root])

client.delete("/foo", rev)
print "Deleted /foo"

foo = client.get("/foo")
print repr(foo)

walk = client.walk("/**")
for f in walk:
    print ' '.join([f.path, str(f.rev), f.value])

client.disconnect()
