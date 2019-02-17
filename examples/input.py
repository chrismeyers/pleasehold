import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()

    with pleasehold.hold('starting', 'complete', delay=0.1) as holding:
        time.sleep(2)
        with pleasehold.transfer(holding):
            stdin = input('enter a push notification: ')
        holding.push(stdin)
        time.sleep(2)

    print(f'time elapsed: {time.time() - before}')
