#!/usr/bin/env python3

import os
os.environ['MPLBACKEND'] = 'module://plutoid.matplotlib_backend'

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import sys
import builtins
import logging
import traceback
from io import StringIO
from blinker import signal

from .stream import OutStream
from .monitor import ExecutionTimeMonitor, CodeExecutionTimeExceeded

logger = logging.getLogger(__name__)

class Executor(object):
    def __init__(self, input_cb=None, max_code_execution_time=0):
        self.input_cb = input_cb
        self.max_code_execution_time = max_code_execution_time

        self.globals = {}
        self.locals = {}

        self.orig_env = {}
        self.orig_env["stdout"] = sys.stdout
        self.orig_env["stderr"] = sys.stderr
        self.orig_env["stdin"] = sys.stdin
        self.orig_env["input"] = builtins.input

        if max_code_execution_time:
            self.execution_time_monitor = ExecutionTimeMonitor(max_code_execution_time)


    def input_trap(self, prompt):
        signal('plutoid::code_execution_pause').send('plutoid')

        self.input_cb(prompt)

        signal('plutoid::code_execution_resume').send('plutoid')


    def exec_code(self, code, tests=[]):
        self.prepare_env()
        signal('plutoid::code_execution_start').send('plutoid')

        has_error = False

        try:
            ast = compile(code, 'your-code', 'exec')
            exec(ast, self.globals)

            for test in tests:
                result='ok'
                ast = compile( test, 'tests', 'exec')

                try:
                    exec( ast, self.globals)
                except AssertionError:
                    result='not-ok'

                signal('plutoid::test_result').send('plutoid', content=test, result=result)

        except CodeExecutionTimeExceeded:
            has_error = True
            sys.stderr.write('Code is executing for too long (>%d secs). Quota over.\n' % self.max_code_execution_time)
        except:
            has_error = True
            self.print_exception()
        finally:
            self.revert_env()
            signal('plutoid::code_execution_end').send('plutoid')

        return has_error


    def print_exception(self):
        chunks = traceback.format_exception(*sys.exc_info())
        chunks = [chunks[0]] + chunks[2:]
        sys.stderr.write(''.join(chunks))


    def prepare_env(self):
        sys.stdout = OutStream('stdout')
        sys.stderr = OutStream('stderr')
        sys.stdin = StringIO()
        builtins.input = self.input_cb


    def revert_env(self):
        sys.stdout = self.orig_env["stdout"]
        sys.stderr = self.orig_env["stderr"]
        sys.stdin = self.orig_env["stdin"]
        builtins.input = self.orig_env["input"]