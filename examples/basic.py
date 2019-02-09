import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()
    
    please_hold = pleasehold.PleaseHold(delay=0.5, symbol='=')

    please_hold.start('starting')
    time.sleep(4) # Simulates long running process
    please_hold.end('end')
    
    please_hold.loading_symbol = '.'
    please_hold.loading_delay = 2.0
    please_hold.start('props changed')
    time.sleep(4) # Simulates long running process
    please_hold.end('end')
    
    # TODO: Handle stdin (sudo prompt). Pause loading?
    
    print(time.time() - before)
