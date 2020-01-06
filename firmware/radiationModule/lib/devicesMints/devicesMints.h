#ifndef DEVICES_MINTS_H
#define DEVICES_MINTS_H

#include <Arduino.h>
// #include <Time.h>

#include "jobsMints.h"



#define CONV_FACTOR 0.00812

extern uint8_t PPD42NSPinMid;
extern uint8_t PPD42NSPinPM10;
bool initializePPD42NSDuoMints();
void readPPD42NSDuoMints(uint8_t sampleTimeSeconds);


extern uint8_t LIBRADPin;
extern long    LIBRADCount;
bool initializeLIBRADMints();
void countPulseLIBRADMint();
void readLIBRADMints(uint8_t sampleTimeSeconds);



#endif
