
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
from collections import OrderedDict

dataFolder    =  mD.dataFolder
airMarPort    =  mD.airMarPort


def main():

    ser = serial.Serial(
    port= airMarPort,\
    baudrate=4800,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    lastHCHDT = time.time()
    lastWIMWV = time.time()
    lastGPGGA = time.time()
    lastGPVTG = time.time()
    lastGPZDA = time.time()
    lastWIMDA = time.time()
    lastYXXDR = time.time()

    delta  = 1
    print("connected to: " + ser.portstr)

    #this will store the line
    line = []
    while True:
        try:
            for c in ser.read():
                line.append(chr(c))
                if chr(c) == '\n':
                    dataString     = (''.join(line)).replace("\r\n","")
                    dateTime  = datetime.datetime.now()

                    if (dataString.startswith("$HCHDT") and mSR.getDeltaTime(lastHCHDT,delta)):
                        mSR.HCHDTWrite(dataString,dateTime)
                        lastHCHDT = time.time()
                        # print(str(dataString))

                    if (dataString.startswith("$WIMWV") and mSR.getDeltaTime(lastWIMWV,delta)):
                        mSR.WIMWVWrite(dataString,dateTime)
                        lastWIMWV = time.time()
                        # print(str(dataString))

                    if (dataString.startswith("$GPGGA") and mSR.getDeltaTime(lastGPGGA,delta)):
                        mSR.GPGGAWrite(dataString,dateTime)
                        lastGPGGA = time.time()
                        # print(str(dataString))

                    if (dataString.startswith("$GPVTG") and mSR.getDeltaTime(lastGPVTG,delta)):
                        mSR.GPVTGWrite(dataString,dateTime)
                        lastGPVTG = time.time()
                        # print(str(dataString))

                    if (dataString.startswith("$GPZDA") and mSR.getDeltaTime(lastGPZDA,delta)):
                        mSR.GPZDAWrite(dataString,dateTime)
                        lastGZDA = time.time()
                        # print(str(dataString))

                    if (dataString.startswith("$WIMDA") and mSR.getDeltaTime(lastWIMDA,delta)):
                        mSR.WIMDAWrite(dataString,dateTime)
                        lastWIMDA = time.time()
                        # print(str(dataString))

                    if (dataString.startswith("$YXXDR,") and mSR.getDeltaTime(lastYXXDR,delta)):
                        mSR.YXXDRWrite(dataString,dateTime)
                        lastYXXDR = time.time()
                        # print(str(dataString))

                    line = []
                    break
        except:
            print("Incomplete String Read")
            line = []

    ser.close()



if __name__ == "__main__":
   main()