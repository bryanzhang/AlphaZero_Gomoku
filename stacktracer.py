#! /usr/bin/python3

import sys
import signal
import traceback
import threading

def _dump_stack_traces(signal_number, frame):
    print(f"\nReceived signal {signal_number}. Dumping stack traces:")
    for thread_id, stack in sys._current_frames().items():
        try:
            thread = threading._active.get(thread_id, None)
            thread_name = thread.name if thread else 'Unknown'
        except Exception:
            thread_name = 'Unknown'

        print(f"\nThread ID: {thread_id} ({thread_name})", file=sys.stderr)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            print(f'  File "{filename}", line {lineno}, in {name}', file=sys.stderr)
            if line:
                print(f"    {line.strip()}", file=sys.stderr)

def register_stack_trace_dump(signal_number=signal.SIGRTMIN + 1):
    """
    注册信号处理器，当接收到指定的信号时打印所有线程的堆栈追踪。

    参数：
        signal_number (int): 要监听的信号，默认是 signal.SIGRTMIN+1。
    """
    signal.signal(signal_number, _dump_stack_traces)
    print(f"Registered stack trace dump on signal {signal_number}.")
