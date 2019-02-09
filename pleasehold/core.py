import threading
import time

class PleaseHold():
    def __init__(self, delay=1.0, symbol='.'):
        self._loading_thread = threading.Thread(name='loading', target=self._loading)
        self._loading_delay = delay
        self._loading_symbol = symbol
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
        print(msg, end='', flush=True)
        
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
        
        
    def _loading(self):
        while self._event.is_set():
            print(self._loading_symbol, end='', flush=True)
            time.sleep(self._loading_delay)
