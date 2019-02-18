class StreamTee(object):
    '''Forks a stream, allowing you to capture output while still displaying
    output in the terminal.

    See: http://www.tentech.ca/2011/05/stream-tee-in-python-saving-stdout-to-file-while-keeping-the-console-alive/

    Args:
        stream1 (:obj:`TextIOWrapper`): The original stream (ex: stdin, stdout)
        stream2 (:obj:`StringIO`): A fork of the original stream
        symbol (str, optional): The loading symbol set in the current instance
            of PleaseHold
    '''
    def __init__(self, stream1, stream2, symbol='.'):
        self._stream1 = stream1
        self._stream2 = stream2
        self.__missing_method_name = None # Hack!
        self._loading_symbol = symbol
        self._num_inputs = 0

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        self.__missing_method_name = name # Could also be a property
        return getattr(self, '__methodmissing__')

    def __methodmissing__(self, *args, **kwargs):
        '''Callback for events coming from the original stream'''
        if (len(args) > 0 and args[0] != '\n' and args[0] != ''
                and args[0] != self._loading_symbol):
            self._num_inputs += 1

        # Emit method call to the forked stream
        callable2 = getattr(self._stream2, self.__missing_method_name)
        callable2(*args, **kwargs)

        # Emit method call to stream 1
        callable1 = getattr(self._stream1, self.__missing_method_name)
        return callable1(*args, **kwargs)

    @property
    def num_inputs(self):
        '''Gets the number of inputs that have occurred during the Transfer
        context'''
        return self._num_inputs
