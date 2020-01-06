
#include "devicesMints.h"

bool initializePPD42NSDuoMints(){
      pinMode(PPD42NSPinMid,INPUT);
      pinMode(PPD42NSPinPM10,INPUT);
      delay(1);
      return true;
    }


void readPPD42NSDuoMints(uint8_t sampleTimeSeconds)
  {
      unsigned long starttime;
      unsigned long sampletime_ms = sampleTimeSeconds*1000;

      float ratioPmMid   = 0;
      float ratioPm10  = 0;

      float concentrationPmMid = 0;
      float concentrationPm2_5 = 0;
      float concentrationPm10  = 0;

      boolean pmMidPinValue = HIGH;
      boolean pm10PinValue = HIGH;

      boolean pmMidReading  = false;
      boolean pm10Reading  = false;

      unsigned long LPOPmMid  =  0;
      unsigned long LPOPm10 =  0;

      unsigned long readingTimePmMid   =  0;
      unsigned long readingTimePm10  =  0;

      starttime = millis();

      while ((millis() - starttime) < sampletime_ms)
      {
         pmMidPinValue =  digitalRead(PPD42NSPinMid);
         pm10PinValue  =  digitalRead(PPD42NSPinPM10);

  //      For Mid Range Readings
         if(pmMidPinValue == LOW && pmMidReading == false) {
            pmMidReading = true;
            readingTimePmMid = micros();
         }

         if(pmMidPinValue == HIGH && pmMidReading == true) {
            LPOPmMid = LPOPmMid + (micros() - readingTimePmMid);
            pmMidReading = false;
         }

  //      For PM 10 Readings
         if(pm10PinValue == LOW && pm10Reading == false) {
            pm10Reading = true;
            readingTimePm10 = micros();
         }

         if(pm10PinValue == HIGH && pm10Reading == true) {
           LPOPm10 = LPOPm10 + (micros() - readingTimePm10);
           pm10Reading = false;
         }

      }// WHILE LOOP END

      ratioPmMid  = LPOPmMid/(sampletime_ms*10.0);
      ratioPm10   = LPOPm10/(sampletime_ms*10.0);

      concentrationPmMid = 1.1*pow(ratioPmMid,3)-3.8*pow(ratioPmMid,2)+520*ratioPmMid+0.62; // using spec sheet curve
      concentrationPm10  = 1.1*pow(ratioPm10,3)-3.8*pow(ratioPm10,2)+520*ratioPm10+0.62; // using spec sheet curve
      concentrationPm2_5 = concentrationPm10 - concentrationPmMid ;


    String readings[8] = {
                          String(sampleTimeSeconds),
                          String(LPOPmMid),
                          String(LPOPm10),
                          String(ratioPmMid,2) ,
                          String(ratioPm10,2),
                          String(concentrationPmMid,2),
                          String(concentrationPm2_5,2),
                          String(concentrationPm10,2)
                        };
                        
    sensorPrintMints("PPD42NSDuo",readings,8);

  }


// // LIBRad ---------------------------------------

bool initializeLIBRADMints(){
    pinMode(LIBRADPin, INPUT);
    digitalWrite(LIBRADPin,HIGH);
    delay(1);
    return true;
  }

void countPulseLIBRADMints(){

      detachInterrupt(0);
      LIBRADCount++;
      while(digitalRead(LIBRADPin)==0){
      }
      attachInterrupt(0,countPulseLIBRADMints,FALLING);
}

void readLIBRADMints(uint8_t sampleTimeSeconds)  {

    LIBRADCount = 0;

    unsigned long sampleTimeMS = sampleTimeSeconds*1000;
    unsigned long startTime = millis();
    attachInterrupt(0,countPulseLIBRADMints,FALLING);
    while ((millis()-startTime) < sampleTimeMS) {
    }
    detachInterrupt(0);
    unsigned long timeSpent = millis()-startTime;

    float countPerMinute = (float(LIBRADCount)*float(60000))/float(timeSpent) ;
    float radiationValue = countPerMinute*CONV_FACTOR;
    String readings[4] = { String(countPerMinute,4), String(radiationValue,4), String(timeSpent),String(LIBRADCount)};
    sensorPrintMints("LIBRAD",readings,4);

}


