import os
os.environ['MPLBACKEND'] = 'module://matplotlib_backend'

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import sys
import builtins

import stream

orig_env = {}
orig_env["stdout"] = sys.stdout
orig_env["stderr"] = sys.stderr
orig_env["input"] = builtins.input


def prepare_env(input_cb):
    sys.stdout = stream.OutStream('stdout')
    sys.stderr = stream.OutStream('stderr')
    builtins.input = input_cb
    
def revert_env():
    sys.stdout = orig_env["stdout"]
    sys.stderr = orig_env["stderr"]
    builtins.input = orig_env["input"]