""" PhatStat Watchdog """

import time

import RPi.GPIO as GPIO

WD_STATUS_PIN = 19
WD_ENABLE_PIN = 26
WD_KICK_PIN = 16

class Watchdog(object):
    """ watchdog base class, non latching. """

    def __init__(self):
        self.enabled = False
        return

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(WD_STATUS_PIN, GPIO.IN)
        GPIO.add_event_detect(WD_STATUS_PIN, GPIO.FALLING)
        GPIO.setup(WD_ENABLE_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(WD_KICK_PIN, GPIO.OUT, initial=GPIO.LOW)

        return self

    def __exit__(self, type, value, traceback):
        self.disable()

        GPIO.cleanup(WD_STATUS_PIN)
        GPIO.cleanup(WD_ENABLE_PIN)
        GPIO.cleanup(WD_KICK_PIN)
        return

    def enable(self, wait=False):
        """ enable watchdog timer allowing digital ouputs
        if wait is set True, then wait until fully initialized (about 300mS)
        else return imediately """
        self.update(0)
        GPIO.output(WD_ENABLE_PIN, GPIO.HIGH)
        self.update(1)
        flush = self.tripped
        self.update(0)

        if wait is True:
            time.sleep(0.3)
            self.update(1)
            flush = self.tripped

        self.enabled = True
        print('watchdog: woke')
        return

    def disable(self):
        """ disable watchdog timer, forcing digital outputs off."""
        GPIO.output(WD_ENABLE_PIN, GPIO.LOW)
        if self.enabled:
            print('watchdog: sleep')

        self.enabled = False
        return

    @property
    def tripped(self):
        """ return true if watchog has tripped since last check or is currently tripped. """
        status = False

        if GPIO.event_detected(WD_STATUS_PIN):
            status = True
        elif GPIO.input(WD_STATUS_PIN) == GPIO.LOW:
            status = True
        return status

    def update(self, state):
        """ update watchdog with new state.
        watchdog requires a 1,0,1,0,... pattern to remain active, enabling outputs.
        watchdog will trip, disabling digital outputs if not updated at least every 1.3 seconds.
        watchdog will reenable outputs once pattern resumes.  This is a non-latching watchdog."""

        # lvc175 clock input is rising edge sensitive
        if state == 1:
            GPIO.output(WD_KICK_PIN, GPIO.HIGH)
        elif state == 0:
            GPIO.output(WD_KICK_PIN, GPIO.LOW)
        else:
            return False

        return True
