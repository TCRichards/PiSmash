# "Technical Objectives for Smash Analysis Project
### Last edited Saturday, June 27, 2019

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

## 2.	Gather massive amounts of training data
### Status: Complete
**a.**	For one month, we captured screenshots of gameplay every three seconds using the Raspberry Pi's camera.  I wrote a
    Python sketch to automatically upload these screenshots to a repository in Google Drive, where they were later manually labeled.
![data gathering](https://raw.githubusercontent.com/TCRichards/PiSmash/master/READMEImages/dataGatheringSetup.jpg)



## 3.	Capture data from Wi-Fi and funnel into Python sketch on a host computer:
### Status: Complete

  **a.**	The Raspberry Pi streams video to a rtsp server using the uv4l library.  The following example was used to set up Pi: https://www.linux-projects.org/uv4l/tutorials/rtsp-server/
  **b.**	The PC running the sketch can capture this rtsp stream using VLC's Python library.  This was very straightforward to accomplish.


## 4.	Use Deep Learning to continuously classify screenshots from the game:
### Status: Complete

  **a.**	Use image classification to detect constantly monitor the status of the game and detect the victory screen.   
    **i.** Make neural network capable of choosing between [Character Select, Stage Select, Pre-Game, Game, Victory, Results, TV OFF, and Menu Screens] (this works surprisingly well).

![Screen Classification](https://raw.githubusercontent.com/TCRichards/PiSmash/master/READMEImages/ScreenClassTest.png)
    **ii.** Make neural network capable of detecting player icons (Not implemented - would be cool to tell who killed whom)
  **b.**	Use text recognition to gather data on damage and kills within each panel   
    **i.**	Google Vision API provides incredible text recognition ability for relatively cheaply ($1.50 for 1000 images analyzed).  We're going with this approach 'for now'
    **ii.** There's lots of information online about the open-source OpenCV library, but after a week of trying to run text recognition and getting terrible results, I opted for Google Vision.  
    **iii.** Once the results screen is detected, use location of player text  (specifically 'P#') to segment screen into a separate panel for each player.    


## 5.	Create Website!
### Status: In progress

   **a.**	Website's backend will store the database with all smash data.  
   **b.**	Website's frontend will provide an interface for users to access to see all statistics
        **i.**	Provide capabilities for determining probabilities based on certain matchups, record the characters played in all games to provide substantially improved control over Smash's built-in statistics."

## 6.	Send detections and processed data from host computer to database:
### Status: Not started

   **a.**	It doesn't look like there's a way for a website to store it's own data file, so instead we can have the computer serving the website locally store a database with all data logged.  Whenever the website is launched, a JavaScript callback will retrieve the data from the server and update the website.

## 7.	Gather data from Server
### Status: Not Started

  **a.**	Have the Raspberry Pi also continually monitor the website backend's database and alert players when there is a change (maybe blinking LED?)
