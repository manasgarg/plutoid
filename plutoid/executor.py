#!/usr/bin/env python3

import env
from blinker import signal

def exec_code(code, input_cb):
    env.prepare_env(input_cb)
    try:
        exec(code)
    except Exception as e:
        exception = signal('plutoid::exception')
        exception.send('plutoid', exception=e)
    finally:
        env.revert_env()
