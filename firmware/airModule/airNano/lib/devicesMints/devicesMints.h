#ifndef DEVICES_MINTS_H
#define DEVICES_MINTS_H
//
#include <Arduino.h>
#include "OPCN3NanoMints.h"
#include "MutichannelGasSensor.h"
#include "Seeed_HM330X.h"
#include "Adafruit_Sensor.h"
#include "Seeed_BME280.h"
#include "SparkFun_SCD30_Arduino_Library.h"
#include "jobsMints.h"




// void sendCommand2DevicesMints(String command);
//
// void setTimeMints(String command);
// void printTimeMints();
// void printTimeOnlyMints();
//
// extern bool serialOut;

// //

extern BME280 bme280;
bool initializeBME280Mints();
void readBME280Mints();
//
bool initializeMGS001Mints();
void readMGS001Mints();
//

extern HM330X hm3301;
extern u8 hm3301Data[30];
bool initializeHM3301Mints();
void readHM3301Mints();


// extern SCD30 scd;
// bool initializeSCD30Mints();
// void readSCD30Mints();


//
extern SCD30 scd;
bool initializeSCD30Mints();
void readSCD30Mints();



// //
extern OPCN3NanoMints opc;
bool initializeOPCN3Mints();
void readOPCN3Mints();

// extern Adafruit_INA219 ina;
// bool initializeINA219Mints();
// void readINA219Mints();


// void printInput(String command);
// void sensorPrintMints(String sensor,String readigs[],uint8_t numOfvals);




















#endif
