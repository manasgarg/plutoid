#!/usr/bin/env python3

from blinker import signal

class OutStream(object):
    def __init__(self, stream_name):
        self.stream_name = stream_name
    
    def write(self, s):
        stream_data = signal('plutoid::%s' % self.stream_name)
        stream_data.send('plutoid', content=s)
    
    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush( self):
        pass

    def truncate(self):
        pass