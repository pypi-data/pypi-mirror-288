# SL400 BornHack 2024 phonebook converter
Convert the BornHack 2024 phonebook JSON to vCard for the Gigaset SL400 DECT handset. It probably also works with the handsets that have been tested with QuickSync4Linux and other Gigaset handsets that have USB.

## Dependencies
* requests
* vobject
* QuickSync4Linux: https://github.com/schorschii/QuickSync4Linux

## Install 
```
git clone https://codeberg.org/eloy/bornhack_sl400
pip3 install -r requirements
```
It writes to the `stdout`, which can be used as `stdin` for `QuickSync4Linux`. Make sure QuickSync4Linux is installed and the permissions for the serial device are correct. 

## Run
Assuming both repositories were put in the home directory, run:

```
~/bornhack_sl400/converter.py | ~/QuickSync4Linux/quicksync.py createcontacts --file - 
```
