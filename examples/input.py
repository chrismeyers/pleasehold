import time
import pleasehold

if __name__ == '__main__':
    print('before')
    before = time.time()

    with pleasehold.hold('starting', 'complete', symbol='#') as holding:
        time.sleep(2)
        with pleasehold.transfer(holding) as t:
            stdin1 = input('enter a push notification: ')
            stdin2 = input('enter another push notification: ')
            stdin3 = input('enter a third push notification: ')
        holding.push(stdin1)
        holding.push(stdin2)
        holding.push(stdin3)

        time.sleep(2)
        with pleasehold.transfer(holding) as t:
            input('this won\'t be pushed: ')
        time.sleep(2)

        # NOTE: The sudo password prompt interacts directly to /dev/tty, so it
        # won't be picked up through StreamTee and cleaned up automatically.

    print(f'time elapsed: {time.time() - before}')
