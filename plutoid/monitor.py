from blinker import signal as blinker_signal
import signal
import time
import logging

logger = logging.getLogger(__name__)


class CodeExecutionTimeExceeded(Exception):
    pass


def raise_execution_time_exception(signum, frame):
    raise CodeExecutionTimeExceeded()


signal.signal(signal.SIGALRM, raise_execution_time_exception)


class ExecutionTimeMonitor(object):
    def __init__(self, max_code_execution_time):
        self.max_code_execution_time = max_code_execution_time

        blinker_signal('plutoidkernel::code_execution_start').connect(self.code_execution_start)
        blinker_signal('plutoidkernel::code_execution_pause').connect(self.code_execution_pause)
        blinker_signal('plutoidkernel::code_execution_resume').connect(self.code_execution_resume)
        blinker_signal('plutoidkernel::code_execution_end').connect(self.code_execution_end)

        self.start_time = 0
        self.remaining_code_execution_time = self.max_code_execution_time


    def code_execution_start(self, sender):
        self.start_time = time.time()
        signal.alarm(self.remaining_code_execution_time)


    def code_execution_pause(self, sender):
        self.remaining_code_execution_time = int(self.remaining_code_execution_time - (time.time() - self.start_time)) + 1
        signal.alarm(0)


    def code_execution_resume(self, sender):
        signal.alarm(self.remaining_code_execution_time)


    def code_execution_end(self, sender):
        self.remaining_code_execution_time = self.max_code_execution_time
        signal.alarm(0)