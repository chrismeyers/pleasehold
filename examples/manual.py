import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()

    holding = pleasehold.hold('starting', 'complete')

    holding.start()
    time.sleep(2)
    holding.push('1')
    holding.push('2')
    holding.push('3')
    holding.push('4')
    time.sleep(2)
    holding.push('another push')
    time.sleep(2)
    holding.end()

    holding.end_msg = 'end'
    holding.delay = 0.1
    holding.symbol = '#'

    holding.start(msg='props changed')
    time.sleep(2)
    holding.push('pushed something')
    time.sleep(2)
    holding.end()

    print(f'time elapsed: {time.time() - before}')
