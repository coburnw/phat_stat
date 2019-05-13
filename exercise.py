if __name__ == '__main__':
    import time
    import signal
    import sys

    from watchdog import Watchdog as Watchdog
    from digital_output import DigitalOutput as DigitalOutput

    def signal_handler(sig, frame):
        myOutput.cleanup()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    print('Ctrl+C to exit')

    with Watchdog() as watchdog:
        watchdog.enable(wait=True)
        myOutput = DigitalOutput(0)
        myOutput.enable()
        increment = 0.1
        delay = 1.0
        while True:
            if delay > 3.0 or delay < 1.0:
                increment = -increment

            if myOutput.is_on():
                watchdog.update(0)
                myOutput.off()
                state = 'off'
            elif myOutput.is_off():
                watchdog.update(1)
                myOutput.on()
                state = 'on'

            if watchdog.tripped:
                print('{:2.1f} ouch!'.format(delay))
                #watchdog.disable()
            else:
                print('{:2.1f} {}'.format(delay, state))

            delay += increment
            time.sleep(delay)
