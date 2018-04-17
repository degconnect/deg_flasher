DEG FLASHER
===========

Tool for flashing AMD RX Series cards(RX 470, RX 480, RX 570, RX 580) so they can mine at better hashing powers.

For now, Degflasher only works on [Ethos](https://www.ethosdistro.com)

It goes to a backend server(http://flasher.degconnect.com/) to check if modded BIOS is already there and download and flash the card with the modded ROM.

If the modded BIOS is not there it will backup anyways the BIOS to http://flasher.degconnect.com/ and it will alert Degconnect team so they can tweek the BIOS as soon as possible. Once that the team updates the system with the modded BIOS a message es sent to the user who ask for that BIOS.


## Installation

pip install https://github.com/degconnect/deg_flasher/archive/master.zip

## How to use it

### Go to ethos console and type:
1. Buy credits at [flasher.degconnect.com](http://flasher.degconnect.com)
2. disallow && r
3. degflasher
4. adjust globalcore and globalmem or mem/cor <hostname> if you have different cards in local.conf
5. allow && r

## Known issues

* Doesn't work after the miner have been running for a while so use disallow && r before using degflasher
* Doesn't work when miner is still running



