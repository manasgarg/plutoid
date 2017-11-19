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

logger = logging.getLogger(__name__)

class Executor(object):
    def __init__(self, input_cb=None):
        self.input_cb = input_cb

        self.globals = {}
        self.locals = {}

        self.orig_env = {}
        self.orig_env["stdout"] = sys.stdout
        self.orig_env["stderr"] = sys.stderr
        self.orig_env["stdin"] = sys.stdin
        self.orig_env["input"] = builtins.input


    def input_trap(self, prompt):
        signal('plutoid::code_execution_pause').send('plutoid')

        self.input_cb(prompt)

        signal('plutoid::code_execution_resume').send('plutoid')


    def exec_code(self, code, tests=[]):
        self.prepare_env()
        signal('plutoid::code_execution_start').send('plutoid')

        exc = None

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

        except Exception as e:
            self.print_exception()
            exc = e
        finally:
            self.revert_env()
            signal('plutoid::code_execution_end').send('plutoid')

        return exc


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