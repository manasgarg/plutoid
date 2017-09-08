from blinker import signal
from plutoid.executor import Executor

stdout_chunks = []
stderr_chunks = []


def stdout_listener(sender, content):
    stdout_chunks.append(content)


def stderr_listener(sender, content):
    stderr_chunks.append(content)


def setup_module():
    signal('plutoid::stdout').connect(stdout_listener)
    signal('plutoid::stderr').connect(stderr_listener)


def setup_function():
    global stderr_chunks, stdout_chunks

    stdout_chunks = []
    stderr_chunks = []


def collect_stdout():
    return ''.join(stdout_chunks)


def collect_stderr():
    return ''.join(stderr_chunks)


def test_stdout():
    code = '''
print('hello')
'''

    e = Executor()
    e.exec_code(code)
    assert collect_stdout() == 'hello\n'


def test_multiline_stdout():
    code = '''
print('hello')
print('world')
'''

    e = Executor()
    e.exec_code(code)
    assert collect_stdout() == 'hello\nworld\n'


def test_multiline_stderr():
    code = '''
import sys
sys.stderr.write('hello')
sys.stderr.write(', world')
'''

    e = Executor()
    e.exec_code(code)
    assert collect_stderr() == 'hello, world'


def test_multi_exec():
    code1 = 'i=2'
    code2 = 'print(i)'

    e = Executor()
    e.exec_code(code1)
    e.exec_code(code2)

    assert collect_stdout() == '2\n'


def test_exception():
    code = '''print(10'''

    e = Executor()
    e.exec_code(code)
    assert collect_stderr().find('Traceback') == 0


def test_input():
    code = '''
s = input('enter something: ')
print(s)
'''

    def input_cb(prompt):
        return 'xyz'

    e = Executor(input_cb)
    e.exec_code(code)
    assert collect_stdout() == 'xyz\n'
