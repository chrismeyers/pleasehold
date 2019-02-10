import sys
import threading
import time

class PleaseHold():
    def __init__(self, delay=1.0, symbol='.'):
        self._loading_thread = threading.Thread(name='loading', target=self._loading)
        self._loading_delay = delay
        self._loading_symbol = symbol
        self._loading_msg = ''
        self._loading_lock = threading.RLock()
        self._event = threading.Event()

    
    @property
    def loading_delay(self):
        return self._loading_delay
    
        
    @loading_delay.setter
    def loading_delay(self, value):
        self._loading_delay = value
        
    
    @property
    def loading_symbol(self):
        return self._loading_symbol
        
        
    @loading_symbol.setter
    def loading_symbol(self, value):
        self._loading_symbol = value
        
        
    def start(self, msg):
        self._loading_msg = msg
        print(self._loading_msg, end='', flush=True)
        
        self._event.set()
        
        if not self._loading_thread.is_alive():
            try:
                self._loading_thread.start()
            except RuntimeError:
                self._loading_thread = threading.Thread(name='loading', target=self._loading)
                self._loading_thread.start()
                
        
    def end(self, msg):
        print(msg, flush=True)
        self._event.clear()
        
        
    def push(self, msg):
        with self._loading_lock:
            sys.stdout.write('\033[K') # Clear the line
            sys.stdout.write('\033[F') # Move up one line
            sys.stdout.write('\n')     # Put pushed message on new line
            print(msg)
            print(self._loading_msg, end='')


    def _loading(self):
        while self._event.is_set():
            with self._loading_lock:
                self._loading_msg += self._loading_symbol
                print(self._loading_symbol, end='', flush=True)
            time.sleep(self._loading_delay)
