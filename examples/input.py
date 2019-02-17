import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()

    with pleasehold.hold('starting', 'complete') as holding:
        time.sleep(2)
        with pleasehold.transfer(holding) as t:
            stdin1 = t.input('enter a push notification: ')
            stdin2 = t.input('enter another push notification: ')
        holding.push(stdin1)
        holding.push(stdin2)
        time.sleep(2)

    print(f'time elapsed: {time.time() - before}')
