#include <Arduino.h>
#include <Wire.h>
#include <devicesMints.h>
#include <jobsMints.h>

bool PPD42NSOnline;

uint8_t PPD42NSPinMid = 3;
uint8_t PPD42NSPinPM10 = 4;

bool    LIBRADOnline;
uint8_t LIBRADPin   = 2;
long    LIBRADCount = 0;

unsigned long initializationPeriod = 1500;


void setup() {
  initializeSerialMints();
  delay(1000);
  PPD42NSOnline      = initializePPD42NSDuoMints();
  delay(1000);
  LIBRADOnline       = initializeLIBRADMints();
}


// the loop routine runs over and over again forever:
void loop() {

 if(PPD42NSOnline)
        {
          readPPD42NSDuoMints(30);
        }


  if(LIBRADOnline)
      {
        readLIBRADMints(30);
      }

}
