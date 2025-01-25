# FlyWatch-Flight-Tracker-and-Notification-Web-App

Track any fight with the help of ICAO Code. Alpha check Bearing, Range and Altitude on yourfingertips. Get Call and Email based notification for your favourite flights for Civilian and MIlitary aircrafts such as C17s, il76s etc appearing within custom radius of your city for our fellow planespotters.

Work on Python CLI based script will start first as a prototype for the web application in cli scripts folder.

### CORE PURPOSE

The Tango aim of this project is to create a program that will provide critical intelligence via automated calls and emails to plane spotters of their favourite aircrafts and potentially providing its  legally trackable location Intel  prompting spotters to position themselves at the designated photographing spot before the estimated time of arrival (ETA) of the military jet. It's crucial to note that certain military aircraft, such as the Charlie 17s, have a limited operational window of maximum 2 hours before they are scrambled at other air force stations. For Military Aviation enthusiasts, this limitation poses a significant setback, as it has personally led to missed spotting opportunities. 

That is : Most of the military aircrafts have negative contact in some of the fight radar apps. So If you are not present at the right time, right place with your right camera settings .
You will not get the perfect shot. Airforce works in secrecy, Most of the best things such as when  tally 4 SEPECAT Jaguar fighterjets visited Vadodara happened quite unexpectedly
Some of these rare jets are visible on one platform but not on other and vice versa. As a result, It is extremely difficult to predict its ETA as well.

Some of these jets arrive once in 8 months to max to max 6 years, And not every planespotter has time to hook up to FR24,Radarbox, ADBS Exchange 24x7. 
Also 6 years is a very long time for a fellow planespotter to witness his aircraft girlfriend with its full mighty engines roaring, 7000 RPM taking off after such a long time.

This is a flight tracker & notification sender from a planespotter to planespotters for planespotting! We Got This.

Prepare for the Lima Oscar November Golf End of Time. Over.


### Technology Stack ####

#### Python based DjangoSERVER 
#### C++ based ESP8266 Microcontroller's server for Buzzer Listener.
#### Twilio API Based VoIP Call Alert
#### React Native based Mobile Application frontend for log tracking and more 
#### SQLLite Database
####  Home Server + Static IP for Port forwarding

#### Python : For CLI based testing version of the core functionalities

### Core Modules of the Project ###
The application is divided into 4 Core modules
1. The Python/Django Server
2. Django based APIs and few web views to facilate the user with the current status of the server
3. React Native based mobile application to set user's location, check server status, flight tracker status,  server logs , login and other functionalities
4. ESP8266 Microcontroller programmed in C++ for Buzzer alert when any C17 comes within 250miles of your city

