 #include "SoftwareSerial.h"
#include <Wire.h>
SoftwareSerial serial_connection(10,11);//Create a serial connection with TX and RX on these pins
#define BUFFER_SIZE 64//This will prevent buffer overruns.
char inData[BUFFER_SIZE];//This is a character buffer where the data sent by the python script will go.
char inChar=-1;//Initialie the first character as nothing
int count=0;//This is the number of lines sent in from the python script
int i=0;//Arduinos are not the most capable chips in the world so I just create the looping variable once
const int MPU_addr=0x68;
// Variables that will store sensor data
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
const int buttonPin = 3;
const int FileCloseButtonPin=4; 
int buttonState = 0; // first button for reading data
int FileCloseButtonState=0; //second button for closing the file
String state ="a";  // this is a flag to indicate closing of file
void setup()
{
  Serial.begin(9600);//Initialize communications to the serial monitor in the Arduino IDE
  serial_connection.begin(9600);//Initialize communications with the bluetooth module
  serial_connection.println("Ready!!!");//Send something to just start comms. This will never be seen.
  Serial.println("Started");//Tell the serial monitor that the sketch has started.
    // Start the comunication with the MPU-6050 sensor
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  pinMode(buttonPin, INPUT);

}
void loop()
{
     // Start the transmission with the MPU-6050 sensor
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr,14,true);
    buttonState = digitalRead(buttonPin);// request a total of 14 registers
    FileCloseButtonState=digitalRead(FileCloseButtonPin);
    // Reads the data from the sensor
    AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
    AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
    //Serial.println("ax"); Serial.println(AcX);
    //Serial.println("ay"); Serial.println(AcY);
    //Serial.println("az"); Serial.println(AcZ);
    Serial.print(FileCloseButtonState);
    if (buttonState == 1) {
    Serial.print(buttonState);
    serial_connection.println("S");   //starting of sending one instance of data
    serial_connection.println(AcX);
    serial_connection.println(AcY);
    serial_connection.println(AcZ);
    serial_connection.println(GyX);
    serial_connection.println(GyY);
    serial_connection.println(GyZ);
    serial_connection.println("E"); //ending of one instance of data
    state="C"; // This indicate that we've been reading the data and file can be closed now
    
  } 
  if(FileCloseButtonState == 1) {
    serial_connection.println(state);// indicating to the computer to close the file
    state="K";//DATA STAYS IN BUFFER SO SENDING SOME GARBAGE
    
  }
    
 
    //serial_connection.println("");
    //serial_connection.print("gx"); serial_connection.print(GyX);
    //serial_connection.print("gy"); serial_connection.print(GyY);
    //serial_connection.print("gz"); serial_connection.print(GyZ);
    //This will prevent bufferoverrun errors
    //delay(100);//Pause for a moment 
}
