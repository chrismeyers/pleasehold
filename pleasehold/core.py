import sys
import threading
import time
from . import terminal as term


class PleaseHold():
    def __init__(self, begin_msg='begin', end_msg='end', delay=1.0, symbol='.'):
        self._begin_msg = begin_msg
        self._end_msg = end_msg
        self._delay = delay
        self._symbol = symbol
        self._loading_ticks = ''
        self._loading_thread = threading.Thread(
            name='loading', target=self._loading)
        self._loading_lock = threading.RLock()
        self._loading_event = threading.Event()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.end()

    @property
    def begin_msg(self):
        return self._begin_msg

    @begin_msg.setter
    def begin_msg(self, value):
        self._begin_msg = value

    @property
    def end_msg(self):
        return self._end_msg

    @end_msg.setter
    def end_msg(self, value):
        self._end_msg = value

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def loading_event(self):
        return self._loading_event

    def start(self, msg=None):
        self._begin_msg = msg if msg is not None else self._begin_msg

        print(self._begin_msg, end='', flush=True)

        self._loading_event.set()

        if not self._loading_thread.is_alive():
            try:
                self._loading_thread.start()
            except RuntimeError:
                self._loading_thread = threading.Thread(
                    name='loading', target=self._loading)
                self._loading_thread.start()

    def end(self, msg=None):
        self._end_msg = msg if msg is not None else self._end_msg

        self._loading_event.clear()
        self._loading_thread.join()

        print(self._end_msg, flush=True)

    def push(self, msg):
        with self._loading_lock:
            term.clear_line()
            term.move_line_up()
            term.move_line_down()
            print(msg, flush=True)
            print(f'{self._begin_msg}{self._loading_ticks}', end='', flush=True)

    def _loading(self):
        while self._loading_event.is_set():
            with self._loading_lock:
                self._loading_ticks += self._symbol
                print(self._symbol, end='', flush=True)
            time.sleep(self._delay)


class Transfer():
    def __init__(self, holding):
        self._holding = holding

    def __enter__(self):
        term.move_line_down()
        self._holding.loading_event.clear()
        return self

    def __exit__(self, type, value, traceback):
        for _ in range(2):
            term.clear_line()
            term.move_line_up()
        self._holding.start()


def hold(begin_msg='begin', end_msg='end', delay=1.0, symbol='.'):
    return PleaseHold(begin_msg, end_msg, delay, symbol)


def transfer(holding):
    return Transfer(holding)
