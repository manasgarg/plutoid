# plutoid - a Python micro kernel

`plutoid` is a light-weight Python kernel. It's useful for embedding Python code execution capabilities in different environments. It borrows heavily from `ipython`. In fact, the first version of `ipython` may have looked something like this.

If you are building an programming education app that provides code execution capabilities, you'll find `plutoid` is a lightweight alternative to `ipython`.

Unlike `ipython`, `plutoid` is a library module. It does not provide a shell or any IPC mechanisms. It's main purpose is to capture `stdout`, `stderr` and `matplotlib graphs` and route them using `blinker` signals. It needs to be embedded in an application to be useful.