import sys
import threading
import time
import io
from . import stream_tee
from . import terminal as term


class PleaseHold():
    '''Manages the loading thread and handles pushing notifications.

    This class supports the use of a context manager:
        with pleasehold.hold() as holding:
            ...

    Args:
        begin_msg (str, optional): The message to the left of the loading bar
        end_msg (str, optional): The message to the right of the loading bar
        delay (float, optional):  The delay between printing loading symbols
        symbol (str, optional): The symbol to be used in the loading bar
    '''
    def __init__(self, begin_msg='begin', end_msg='end', delay=1.0, symbol='.'):
        self._begin_msg = begin_msg
        self._end_msg = end_msg
        self._delay = delay
        self._symbol = symbol
        self._loading_ticks = ''
        self._loading_thread = threading.Thread(
            name='loading', target=self._loading)
        self._loading_lock = threading.Lock()
        self._loading_event = threading.Event()

    def __enter__(self):
        '''Starts the loading thread if this class is initialized via a context
        manager
        '''
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        '''Joins the loading thread if this class is initialized via a context
        manager
        '''
        self.end()

    @property
    def begin_msg(self):
        '''str: Gets or sets the message to the left of the loading bar'''
        return self._begin_msg

    @begin_msg.setter
    def begin_msg(self, value):
        self._begin_msg = value

    @property
    def end_msg(self):
        '''str: Gets or sets the message to the right of the loading bar'''
        return self._end_msg

    @end_msg.setter
    def end_msg(self, value):
        self._end_msg = value

    @property
    def delay(self):
        '''float: Gets or sets the delay between printing loading symbols'''
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @property
    def symbol(self):
        '''str: Gets or sets the symbol that's used in the loading bar'''
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def loading_ticks(self):
        '''str: Gets or sets the loading ticks

        NOTE: The setter will always reset _loading_ticks to an empty string!
        '''
        return self._symbol

    @loading_ticks.setter
    def loading_ticks(self, value):
        self._loading_ticks = ''

    @property
    def loading_event(self):
        '''str: Gets the threading.Event() instance used to interact with the
        loading thread
        '''
        return self._loading_event

    def start(self, msg=None):
        '''Starts the loading thread and prints the begin message.

        Args:
            msg (str, optional): Used to override self._begin_msg
        '''
        self._begin_msg = msg if msg is not None else self._begin_msg

        print(f'{self._begin_msg}{self._loading_ticks}', end='', flush=True)

        self._loading_event.set()

        if not self._loading_thread.is_alive():
            try:
                self._loading_thread.start()
            except RuntimeError:
                self._loading_thread = threading.Thread(
                    name='loading', target=self._loading)
                self._loading_thread.start()

    def end(self, msg=None):
        '''Joins the loading thread and prints the end message.

        Args:
            msg (str, optional): Used to override self._end_msg
        '''
        self._end_msg = msg if msg is not None else self._end_msg

        self._loading_event.clear()
        self._loading_thread.join()

        print(self._end_msg, flush=True)

    def push(self, msg):
        '''Pushes a message above the loading bar.

        Args:
            msg (str): The message to push
        '''
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
    '''Pauses the loading thread to allow for user input

    This class supports the use of a context manager:
        with pleasehold.transfer(holding) as t:
            ...

    Args:
        holding (PleaseHold): The instance of PleaseHold that should be paused
    '''
    def __init__(self, holding):
        self._holding = holding
        self._output_stream = io.StringIO()
        self._stream_tee = stream_tee.StreamTee(
            sys.stdout, self._output_stream, holding.symbol)

    def __enter__(self):
        '''Pauses the PleaseHold loading thread and prepares for input if this
        class is initialized via a context manager
        '''
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        '''Cleans up input prompts and resumes the PleaseHold loading thread if
        this class is initialized via a context manager
        '''
        self.end()

    def start(self):
        '''Pauses the PleaseHold loading thread and prepares for input'''
        sys.stdout = self._stream_tee
        term.move_line_down()
        self._holding.loading_event.clear()

    def end(self):
        '''Cleans up input prompts and resumes the PleaseHold loading thread'''
        sys.stdout = sys.__stdout__
        for _ in range(self._stream_tee.num_inputs + 1):
            term.clear_line()
            term.move_line_up()
        self._holding.start()


def hold(begin_msg='begin', end_msg='end', delay=1.0, symbol='.'):
    '''Instantiates an instance of PleaseHold.

    The arguments are passed through to the PleaseHold constructor.

    Args:
        begin_msg (str, optional): The message to the left of the loading bar
        end_msg (str, optional): The message to the right of the loading bar
        delay (float, optional):  The delay between printing loading symbols
        symbol (str, optional): The symbol to be used in the loading bar
    '''
    return PleaseHold(begin_msg, end_msg, delay, symbol)


def transfer(holding):
    '''Instantiates an instance of Transfer.

    The arguments are passed through to the Transfer constructor.

    Args:
        holding (PleaseHold): The instance of PleaseHold that should be paused
    '''
    return Transfer(holding)
