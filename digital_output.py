""" PhatStat DigitalOutput """

import RPi.GPIO as GPIO

# BCM pins used
OUT0_PIN = 12
OUT1_PIN = 13

class DigitalOutput(object):
    """ DigitalOutput abstracts the dirty details.
    channel is either 0 or 1 for Output0 or Output1 """

    def __init__(self, channel):
        GPIO.setmode(GPIO.BCM)

        self._pins = [OUT0_PIN, OUT1_PIN]
        self._off_state = GPIO.LOW
        self._on_state = GPIO.HIGH

        self.pin = self._pins[channel]
        GPIO.setup(self.pin, GPIO.IN)

        print('DigitalOutput: init({})'.format(self.pin))
        return

    def cleanup(self):
        """ release channel resources """
        self.disable()
        GPIO.cleanup(self.pin)
        print('DigitalOutput: cleanup({})'.format(self.pin))
        return

    def enable(self):
        """ enable channel """
        GPIO.setup(self.pin, GPIO.OUT, initial=self._off_state)
        return

    def disable(self):
        """ disable channel """
        self.off()
        GPIO.setup(self.pin, GPIO.IN)
        return

    def on(self):
        """ turn output on (sink current) """
        GPIO.output(self.pin, self._on_state)
        return

    def off(self):
        """ turn output off (high impedance) """
        GPIO.output(self.pin, self._off_state)
        return

    def is_on(self):
        """ return true if output on """
        return GPIO.input(self.pin) == self._on_state

    def is_off(self):
        """ return true if output off """
        return GPIO.input(self.pin) == self._off_state
