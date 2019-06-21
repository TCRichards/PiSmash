# "Technical Objectives for Smash Analysis Project
### Last edited Saturday, June 15, 2019

## 1.	Collect video and audio using Raspberry Pi or microcontroller
### Status: Complete
  **a.**	Default implementation is to use Pi Camera to stream video to a web server:     
    **i.**	Great tutorial found from: https://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android.   
    **ii.**	This guide uses the same techniques as IP cameras use to efficiently send photos over Wi-Fi (sends individual JPEGs which can be converted to video by any browser)   
  **b.**	Could instead just use an IP (internet protocol) security camera:   
    **i.**	Many IP (internet protocol) cameras already exist and already transmit video and audio over the internet. Info on connecting Raspberry Pi to IP camera: https://reolink.com/connect-raspberry-pi-to-ip-cameras   
    **ii.**	P2P (peer-to-peer) IP cameras seem to simplify this connection   
    **iii.**	IP cameras such as Xiaomi's Small Ant (https://www.honorbuy.com/167-ants-xiaoyi-smart-camera.html) are also cheaper than buying a Pi Camera and Pi Microphone combined, and would enable the use of a cheaper microcontroller rather than a Raspberry Pi since the microcontroller wouldn't need to deal directly with video   
    **iv.**	 Our project aside, could we ever sell a security camera for people to put in their houses and have us analyze? Definitely creepy   
  **c.**	Prototype using Pi Camera first and then test other options for cost efficiency?   


## 2.	Send collected video and audio over Wi-Fi:
### Status: Complete; using UV4l library to network stream from RPi

  **a.**	If using IP P2P camera, this is done automatically   
  **b.**	If using Pi Camera, photos are taken continuously and then sent over Wi-Fi using MJPG-Streamer, an open-source streaming library   

## 3.	Capture data from Wi-Fi and funnel into Python sketch on a host computer:
### Status: Nearly complete; can read stream using VLC but choppy method of capturing frames

  **a.**	Video is meant to viewed in a browser. If we liked JavaScript we could use Tensorflow in the browser directly   
    **i.**	https://hackernoon.com/tensorflow-js-real-time-object-detection-in-10-lines-of-code-baf15dfb95b2   
  **b.**	Can collect image data from website using HTTP requests from Python using requests library   
    **i.**	https://www.youtube.com/watch?v=v5TIu67oTWg   


## 4.	Use Deep Learning algorithms to process audio and video: 
### Status: Halfway; Model is made, but can only classify, not detect objects 

  **a.**	Use image recognition to detect victory screen and identify character icons   
    **i.** Make neural network capable of detecting a victory screen    
    **ii.** Make neural network capable of detecting player icons    
    **iii.** Once victory screen is detected, use background colors to segment screen into a separate panel for each player.    
  **b.**	Use text recognition to gather data on damage and kills within each panel   
    **i.**	Michael Reeves (great YouTuber) used Python's optical character recognition (OCR) to read health data from screen: https://www.youtube.com/watch?v=D75ZuaSR8nQ    
    **ii.** OCR libraries can handle the text recognition -- we don't need to make our own network for that            
    **iii.**	pyTesseract seems to be the most common Python OCR library.  Much simpler than Tensorflow since we don't need to train the neural networks, but may require some image processing to get in a readable format    
  **c.**	Use audio recognition to constantly listen for key sounds (spikes)   
    **i.**	Added bonus.  Would require additional hardware for the microphone, so let's work on this once the rest is done.    


## 5.	Create Website!
### Status: Not started

   **a.**	Website's backend will store the database with all smash data.  
   **b.**	Website's frontend will provide an interface for users to access to see all statistics
        **i.**	Provide capabilities for determining probabilities based on certain matchups, record the characters played in all games to provide substantially improved control over Smash's built-in statistics."

## 6.	Send detections and processed data from host computer to database on website's backend:
### Status: Not started

   **a.**	Our website's backend could be a database that each Raspberry Pi monitors.  Easy to write data from PC to database, and have Raspberry Pi register changes.
     **i.**	Ideally would use SQL, but a big spreadsheet wouldn't be terrible
     **ii.**	Since changes are made to database, we can use this master database to run any statistics

## 7.	Gather data from Server
### Status: Not Started

  **a.**	Have the Raspberry Pi also continually monitor the website backend's database and alert players when there is a change (maybe blinking LED?)
