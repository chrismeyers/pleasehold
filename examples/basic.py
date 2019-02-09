import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()
    
    please_hold = pleasehold.PleaseHold(delay=0.5, symbol='=')

    please_hold.start('starting')
    time.sleep(1)
    please_hold.push('this should be above')
    time.sleep(1)
    please_hold.push('another push')
    time.sleep(2)
    please_hold.end('end')
    
    please_hold.loading_symbol = '.'
    please_hold.loading_delay = 2.0
    please_hold.start('props changed')
    time.sleep(2)
    please_hold.push('pushed something')
    time.sleep(2)
    please_hold.end('end')
    
    # TODO: Handle stdin (sudo prompt). Pause loading?
    
    print(time.time() - before)
