# phat_stat
Thermostat for the Raspberry Pi

A pHat-Stat is a temperature controller	interface for your Raspberry Pi in a pHat form factor.  Information about the board itself can be found here: https://www.tindie.com/products/RCW/phat-stat-temperature-controller/

This repository contains Python classes for interacting with the digital outputs and the hardware watchdog timer.

Along with the Digital_Output class used for driving the 40107 digital outputs and the Watchdog class for interacting with the APX823 watchdog, the [MCP342x](https://github.com/coburnw/MCP342x) repository contains classes for interacting with the pHat-Stat's MCP3426 A/D converter.

Additionally I find the following repositories quite helpful in building a full featured temperature controller:
* [NTC_Class](https://github.com/OZ1LQO/NTC_Class) for deriving the cold junction temperature from the onboard B3570 Thermistor resistance
* [thermocouples](https://github.com/jonathanimb/thermocouples) can convert the Thermocouple voltage to temperature including cold junction	compensation
* [ivPID](https://github.com/ivmech/ivPID) for closing the Loop
* dsm to Pulse Width Modulate the digital outputs according to the result of the pid

Be sure to check out [luma.oled](https://github.com/rm-hull/luma.oled) to put that final bit of gloss on your project!
