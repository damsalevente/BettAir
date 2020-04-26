
#include <MQTTClient.h>
#include <ArduinoJson.h>
#include <WiFi101.h>
#include "Adafruit_CCS811.h"


typedef struct rgb
{
  float red;
  float green;
  float blue;
  
}rgb;


/* define ports */
int photoTrans =  A1;
int temperature_pin = A2;
int red_pin = 0; /* tbd */
int green_pin = 0;/* tbd */
int blue_pin = 0;/* tbd */
/* end define ports */

/* variables */
float timestamp_value;
float co2_value;
float tvoc_value;
float temperature_value;
float light_value;
rgb rgb_value;

char _SSID[] = "my secret ssid "; /* for wifi connection check */
char _PASSWORD[]= "my secret password";
/* end variables */

/* included module classes */
WiFiSSLClient ipCloudStack; 
MQTTClient mqttCloudClient; 
Adafruit_CCS811 ccs; /* co2 sensor */
/* end included module classes */


// the setup function runs once when you press reset or power the board
void setup() {
  char mqttCloudServer[]     = "api.artik.cloud"; 
  int  mqttCloudPort         = 8883; 
  char mqttCloudClientName[] = "ARTIK-Arduino"; 
  char mqttCloudUsername[]   = "[device-id]";  
  char mqttCloudPassword[]   = "[device-token]";  
  char mqttCloudDataOut[]    = "/v1.1/messages/[device-id]";  
  /* Wifi Setting */
  WiFi.begin(_SSID, _PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  /* Co2 sensor Setting */
  if(!ccs.begin())
  {
  Serial.println("Failed to start sensor! Please check wiring.");
  while(1);  /* blocking wait */
  }
  
  /*  wait for the sensor to be ready */
  while(!ccs.available());
  /* light sensor settings */
  pinMode(photoTrans, INPUT);
  pinMode(temperature_pin, INPUT);
}

int  generate_ti_stamp(float * ti)
{
  (*ti)++;
  return 0;
}
/* every function from this type should has exlusive acces to the handler object*/
/* function read_co2
* brief: reads ccs811 sensor values and gives through parameters
* parameters: co2: co2 value 
              tvoc: tvoc value
  returns: error code zero if no problem occured
*/
int  read_co2(float *co2, float *tvoc )
{
  int returnCode = 0;
  if(ccs.available())
  {
    if(!ccs.readData())
    {
      *co2 = ccs.geteCO2();
      *tvoc = ccs.getTVOC();
    }
    else
    {
      returnCode = 1;
    }
  }
  else
  {
    returnCode = 2;
  }
  return returnCode;
}
int  read_light(float *light)
{
  *light = analogRead(photoTrans); 
  return 0;
}
int  read_temp(float *temp)
{
  /* todo converting etc. */
  *temp = analogRead(temperature_pin);
  return 0;
}

/* function read data
* brief: gets all the sensor data and generates timestamp 
* parameters: ti: timestamp output pointer
              temp: timestamp output pointer
              co2: co2 value output pointer
              tvoc: tvoc value output pointer
              tvoc: total volatile compund pointer
              light: timestamp output pointer
* output: status tbd what will it mean
*         e.g error 0x01 -> first value is bad 
*/
int read_data(float *ti, float *temp, float *co2,float *tvoc, float *light)
{
  int errorcode = 0x0;
  errorcode |= generate_ti_stamp(ti);
  errorcode |= read_co2(co2,tvoc);
  errorcode |= read_light(light);
  errorcode |= read_temp(temp); 
  return errorcode;
}

void print_values()
{
  Serial.println("Timestamp:");
  Serial.println(timestamp_value);
  Serial.println("Temperature:");
  Serial.println(temperature_value);
  Serial.println("Co2");
  Serial.println(co2_value);
  Serial.println("TvOC");
  Serial.println(tvoc_value);
  Serial.println("light");
  Serial.println(light_value);
}
// the loop function runs over and over again forever
void loop() {
  read_data(&timestamp_value, &temperature_value, &co2_value,&tvoc_value, &light_value); 
  print_values();
  delay(500);
}
