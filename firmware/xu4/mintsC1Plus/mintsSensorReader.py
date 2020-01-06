# ***************************************************************************
#  mintsXU4
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: February 4th, 2019
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************

import serial
import datetime
import os
import csv
import deepdish as dd
from mintsC1Plus import mintsDefinitions as mD
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import netifaces as ni
import math

macAddress    = mD.macAddress
dataFolder    = mD.dataFolder
latestOff     = mD.latestOff




def sensorFinisher(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)

def sensorFinisherIP(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePathIP(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)



def getDeltaTime(beginTime,deltaWanted):
    return (time.time() - beginTime)> deltaWanted

def getLatitudeCords(latitudeStr,latitudeDirection):
    latitude = float(latitudeStr)
    latitudeCord      =  math.floor(latitude/100) +(latitude - 100*(math.floor(latitude/100)))/60
    if(latitudeDirection=="S"):
        latitudeCord = -1*latitudeCord
    return latitudeCord

def getLongitudeCords(longitudeStr,longitudeDirection):
    longitude = float(longitudeStr)
    longitudeCord      =  math.floor(longitude/100) +(longitude - 100*(math.floor(longitude/100)))/60
    if(longitudeDirection=="W"):
        longitudeCord = -1*longitudeCord
    return longitudeCord



def HCHDTWrite(sensorData,dateTime):

    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "HCHDT"
    dataLength = 3

    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    ,str(dateTime)),
        	    ("heading"      ,dataOut[1]),
            	("HID"          ,dataOut[2]),
                ("checkSum"     ,dataOut[3]),
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)

def WIMWVWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "WIMWV"
    dataLength = 6

    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"       ,str(dateTime)),
        	    ("windAngle"      ,dataOut[1]),
            	("WAReference"    ,dataOut[2]),
                ("windSpeed"      ,dataOut[3]),
            	("WSUnits" ,       dataOut[4]),
            	("status"         ,dataOut[5]),
                ("checkSum"       ,dataOut[6]),
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def GPGGAWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "GPGGA"
    dataLength = 15
    gpsQuality = dataOut[6]


    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"              ,str(dateTime)),
        	    ("UTCTimeStamp"          ,dataOut[1]),
            	("latitude"              ,dataOut[2]),
                ("latDirection"          ,dataOut[3]),
                ("longitude"             ,dataOut[4]),
                ("lonDirection"          ,dataOut[5]),
            	("gpsQuality"            ,dataOut[6]),
                ("numberOfSatellites"    ,dataOut[7]),
                ("horizontalDilution"    ,dataOut[8]),
                ("altitude"              ,dataOut[9]),
                ("AUnits"                ,dataOut[10]),
                ("geoidalSeparation"     ,dataOut[11]),
                ("GSUnits"               ,dataOut[12]),
                ("ageOfDifferential"     ,dataOut[13]),
                ("stationID"             ,dataOut[14]),
                ("checkSum"              ,dataOut[15])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def GPSGPGGA2Write(dataString,dateTime):
    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    latitudeCordinate = getLatitudeCords(sensorData.lat,sensorData.lat_dir)

    if(sensorData.gps_qual>0):
        sensorName = "GPSGPGGA2"
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("timestamp"         ,sensorData.timestamp),
                ("latitudeCoordinate" ,getLatitudeCords(sensorData.lat,sensorData.lat_dir)),
                ("longitudeCoordinate",getLongitudeCords(sensorData.lon,sensorData.lon_dir)),
                ("latitude"          ,sensorData.lat),
                ("latitudeDirection" ,sensorData.lat_dir),
                ("longitude"         ,sensorData.lon),
                ("longitudeDirection",sensorData.lon_dir),
                ("gpsQuality"        ,sensorData.gps_qual),
                ("numberOfSatellites",sensorData.num_sats),
                ("HorizontalDilution",sensorData.horizontal_dil),
                ("altitude"          ,sensorData.altitude),
                ("altitudeUnits"     ,sensorData.altitude_units),
                ("undulation"        ,sensorData.geo_sep),
                ("undulationUnits"   ,sensorData.geo_sep_units),
                ("age"               ,sensorData.age_gps_data),
                ("stationID"         ,sensorData.ref_station_id)
        	 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)




def GPVTGWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "GPVTG"
    dataLength = 10
    gpsQuality = dataOut[6]

    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"               ,str(dateTime)),
        	    ("courseOGTrue"           ,dataOut[1]),
            	("relativeToTN"           ,dataOut[2]),
	            ("courseOGMagnetic"       ,dataOut[3]),
                ("relativeToMN"           ,dataOut[4]),
                ("speedOverGroundKnots"   ,dataOut[5]),
            	("SOGKUnits"              ,dataOut[6]),
                ("speedOverGroundKMPH"    ,dataOut[7]),
            	("SOGKMPHUnits"           ,dataOut[8]),
                ("mode"                   ,dataOut[9]),
                ("checkSum"               ,dataOut[10]),
             ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GPZDAWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "GPZDA"
    dataLength = 7
    #
    #

    if(len(dataOut) ==(dataLength +1)):
        year      = int(dataOut[4])
        month     = int(dataOut[3])
        day       = int(dataOut[2])
        hour      = int(dataOut[1][:2])
        minute    = int(dataOut[1][2:4])
        second    = int(dataOut[1][4:6])
        dateTime  = datetime.datetime(year, month,day, hour, minute,second)

        sensorDictionary = OrderedDict([
                ("dateTime"              ,str(dateTime)),
        	    ("UTCTimeStamp"          ,dataOut[1]),
            	("UTCDay"                ,dataOut[2]),
	            ("UTCMonth"              ,dataOut[3]),
        	    ("UTCYear"               ,dataOut[4]),
                ("localHours"            ,dataOut[5]),
          	    ("localMinutes"          ,dataOut[6]),
                ("checkSum"              ,dataOut[7])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)
        return True,dateTime;

    return False,"xxxx"



def TIROTWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "TIROT"
    dataLength = 3

    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"                ,str(dateTime)),
        	    ("rateOfTurn"              ,dataOut[1]),
                ("validity"                ,dataOut[2]),
                ("checkSum"                ,dataOut[3])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)





def WIMDAWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "WIMDA"
    dataLength = 21

    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"                        ,str(dateTime)),
        	    ("barrometricPressureMercury"      ,dataOut[1]),
            	("BPMUnits"                        ,dataOut[2]),
                ("barrometricPressureBars"         ,dataOut[3]),
                ("BPBUnits"                        ,dataOut[4]),
                ("airTemperature"                  ,dataOut[5]),
                ("ATUnits"                         ,dataOut[6]),
                ("waterTemperature"                ,dataOut[7]),
                ("WTUnits"                         ,dataOut[8]),
            	("relativeHumidity"                ,dataOut[9]),
                ("absoluteHumidity"                ,dataOut[10]),
                ("dewPoint"                        ,dataOut[11]),
                ("DPUnits"                         ,dataOut[12]),
                ("windDirectionTrue"               ,dataOut[13]),
                ("WDTUnits"                        ,dataOut[14]),
                ("windDirectionMagnetic"           ,dataOut[15]),
                ("WDMUnits"                        ,dataOut[16]),
                ("windSpeedKnots"                  ,dataOut[17]),
                ("WSKUnits"                        ,dataOut[18]),
                ("windSpeedMetersPerSecond"        ,dataOut[19]),
                ("WSMPSUnits"                      ,dataOut[20]),
                ("checkSum"                        ,dataOut[21])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def YXXDRWrite(sensorData,dateTime):
    dataOut    = sensorData.replace('*',',').split(',')
    sensorName = "YXXDR"
    dataLength = 17

    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"                       ,str(dateTime)),
        	    ("temperature"                    ,dataOut[1]),
            	("relativeWindChillTemperature"   ,dataOut[2]),
                ("TUnits"                         ,dataOut[3]),
                ("RWCTID"                         ,dataOut[4]),
                ("RWCTUnits"                      ,dataOut[5]),
            	("theoreticalWindChillTemperature",dataOut[6]),
                ("TUnits2"                        ,dataOut[7]),
                ("TWCTID"                         ,dataOut[8]),
                ("TWCTUnits"                      ,dataOut[9]),
                ("heatIndex"                      ,dataOut[10]),
                ("HIUnits"                        ,dataOut[11]),
                ("HIID"                           ,dataOut[12]),
                ("pressureUnits"                  ,dataOut[13]),
                ("barrometricPressureBars"        ,dataOut[14]),
                ("BPBUnits"                       ,dataOut[15]),
                ("BPBID"                          ,dataOut[16]),
                ("checkSum"                       ,dataOut[17])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)

def writeCSV2(writePath,sensorDictionary,exists):
    keys =  list(sensorDictionary.keys())
    print("===================================")
    print(writePath)
    print(sensorDictionary)
    with open(writePath, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        # print(exists)
        if(not(exists)):
            writer.writeheader()
        writer.writerow(sensorDictionary)

def getWritePathIP(labelIn,dateTime):
    #Example  : MINTS_0061.csv
    writePath = dataFolder+"/"+macAddress+"/"+"MINTS_"+ macAddress+ ".csv"
    return writePath;

def getWritePath(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) +".csv"
    return writePath;

def getListDictionaryFromPath(dirPath):
    print("Reading : "+ dirPath)
    reader = csv.DictReader(open(dirPath))
    reader = list(reader)

def directoryCheck(outputPath):
    exists = os.path.isfile(outputPath)
    directoryIn = os.path.dirname(outputPath)
    if not os.path.exists(directoryIn):
        os.makedirs(directoryIn)
    return exists
