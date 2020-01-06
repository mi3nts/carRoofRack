#
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import sys


dataFolder  = mD.dataFolder
nanoPorts    = mD.nanoPorts

def main(portNum):
    if(len(nanoPorts)>0):

        ser = serial.Serial(
        port= nanoPorts[portNum],\
        baudrate=9600,\
        parity  =serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0)

        print(" ")
        print("Connected to: " + ser.portstr)
        print(" ")

        #this will store the line
        line = []

        while True:
            try:
                for c in ser.read():
                    line.append(chr(c))
                    if chr(c) == '~':
                        dataString     = (''.join(line))
                        dataStringPost = dataString.replace('~', '')
                        print(dataStringPost)
                        mSR.dataSplit(dataStringPost,datetime.datetime.now())
                        line = []
                        break
            except:
                print("Incomplete String Read")
                line = []
        ser.close()


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    portNum = int(sys.argv[1])
    print("Number of Arduino Nano devices: {0}".format(len(nanoPorts)))
    print("Monitoring Arduino Nano on port: {0}".format(nanoPorts[portNum]))
    main(portNum)
