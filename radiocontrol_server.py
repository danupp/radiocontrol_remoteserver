import string
import time
import math
import smbus
import numpy as np
import socket

bus = smbus.SMBus(1)
fpga_addr = 0x23

if_freq = 45000 # constant
quit_flag = 0
comm_fail = 0


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8899 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except (socket.error , msg):
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
s.listen(0) # Only one connection allowed

while (1):
    # Wait to accept a connection - blocking call
    print ('Server listening.')
    conn, addr = s.accept()
    
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    
    #welcome = "Welcome to the server.\n"
    #conn.sendall(welcome.encode())
    
    # Receiving from client
    while(quit_flag==0):
        rxdata = conn.recv(32).decode()

        print (rxdata)
     
        # Parse received string:
        [cmd, arg] = rxdata.split(" ")[0:2]
        
        if (cmd == "mode"):   
            if (arg == "AM"):
                cmd = 0x40
            elif (arg == "LSB"):
                cmd = 0x70 # Set to LSB
            elif (arg == "USB"):
                cmd = 0x78 # Set to USB
            elif (arg == "CWN"):
                cmd = 0x60 # Set to LSB narrow
            try:
                bus.write_word_data(fpga_addr,cmd,0)
            except:
                comm_fail = 1
        elif (cmd == "freq"):
            freq = float(arg)
            if (freq<0):
                freq = 0
            elif (freq>30000):
                freq=30000
            ftw = (if_freq-freq)*34.9525333333 #pow(2,22)/(6*20000)
            ftw_top = math.floor(ftw/65536) #math.floor(ftw/pow(2,16))
            ftw_bottop = math.floor((ftw-ftw_top*65536)/256) #math.floor((ftw-ftw_top*pow(2,16))/pow(2,8))
            ftw_botbot = round(ftw%256) #round(ftw%pow(2,8))
            try:
                bus.write_word_data(fpga_addr,0xc0 | np.uint8(ftw_top), np.uint16(ftw_botbot*256+ftw_bottop))
            except:
                comm_fail = 1
        elif (cmd == "vol"):
            try:
                bus.write_word_data(fpga_addr,0x07,int(vol))
            except:
                comm_fail = 1
        elif (cmd == "rssi" and arg == "?"):
            try:
                rssi = bus.read_byte(fpga_addr) & 31
                conn.sendall(("rssi " + str(rssi)).encode())
            except:
                comm_fail = 1

