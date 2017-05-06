# Remote control server for the FPGA radio

This contains experimental software for remote control of the FPGA radio. It typically runs on a Raspberry Pi, connected over I2C or UART to the FPGA radio, and opens up ports towards the network for remote control. For client software see experimental support in the GTK app ( https://github.com/danupp/radiocontrol_gtk-app ).

This repository was created 2017-05-06 in order to separate code from the legacy repository containing both FPGA firmware, applet and remote server.
