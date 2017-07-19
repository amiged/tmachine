#!/usr/bin/env python3

import aieye_find


if (__name__ == '__main__'):

    iflist = [] 
    for fname in aieye_find.find('../LogarithmicOperations_FPGA/', '*.*'):
        iflist.append(fname)

    '''
    for fname in aieye_find.find('../PROGRAPE-LinuxDriver/', '*.*'):
        iflist.append(fname)
    '''

    for file in iflist:
        cmd = 'cp %s ./tmp/' % file
        print (cmd)

