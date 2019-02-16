import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()

    with pleasehold.hold('starting', 'complete') as holding:
        time.sleep(2)
        holding.push('1')
        holding.push('2')
        holding.push('3')
        holding.push('4')
        time.sleep(2)
        holding.push('another push')
        time.sleep(2)

    with pleasehold.hold(begin_msg='props changed', delay=0.1, symbol='#') as holding:
        time.sleep(2)
        holding.push('pushed something')
        time.sleep(2)

    # TODO: Handle stdin (sudo prompt). Pause loading?

    print(f'time elapsed: {time.time() - before}')
