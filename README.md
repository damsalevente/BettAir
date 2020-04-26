# BettAIR

Air quality monitoring solution for home office.

Offices and schools must have a solution for air quality and light, but since we are locked in, we have to work/study from home, where noone, but us can handle our environment. Because of this, we propose a small and easy to use IOT tool, which will help us monitor air quality.


We measure CO2, TVOC, Temperature, and light

A little arduiono mkr will send data to the server, which will aggregate store them for later analysation

Used protocol: mqtt
Server: nodejs/python
Mobile client: java

Based on some research, i found a table consisting some red-green result for 8 hour averages, this is what we will report to the client dashboard

if temp is below ... and co2 is above .... and tvoc is above ... then rgb led is ...

One rgb light will indicate the current situation of the room.

# TODO

Currently, everything is in the .ino file 

- conversions from raw adc values to ppm/Celsius etc, with measures 
- seperate header and source files for different sensors
- hold more data, calculate average from it, in order to reduce spikes

- mqtt client  -> big todo
- json library exploration

# Resources 
....
