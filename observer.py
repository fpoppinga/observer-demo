import multiprocessing
import os
import signal
import sys
from time import sleep

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class CallbackEventHandler(PatternMatchingEventHandler):
    def __init__(self, callback):
        PatternMatchingEventHandler.__init__(self, patterns=["*.txt"], ignore_directories=True, case_sensitive=True)
        self.callback = callback

    def on_created(self, event):
        self.callback(event)


class Scheduler:
    def __init__(self):
        self.processes = []

    def schedule(self):
        for i in range(5):
            p = multiprocessing.Process(target=Scheduler._optimize)
            self.processes.append(p)
            p.start()

        # can be before or after starting the processes
        observer = Observer()
        handler = CallbackEventHandler(lambda event: self.abort())
        observer.schedule(handler, "./test", True)
        observer.start()

    @staticmethod
    def _optimize():
        signal.signal(signal.SIGTERM, Scheduler._cleanup)

        for i in range(10):
            print(f"optimizing {os.getpid()}: {i}")
            sleep(1)

    @staticmethod
    def _cleanup(x, y):
        print(f"kill dymola {os.getpid()}: {x}, {y}")
        sys.exit()

    def abort(self):
        for p in self.processes:
            os.kill(p.pid, signal.SIGTERM)


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.schedule()
    # highly complex simulation code
