# Color_Based_Product_Sorter
Color detection is through opencv and numpy operations. We made this as our "Internet of Things" project.It scans an image,detects the color and moves the servo across converyor belt in a particular angle.After all this,values are uploaded to "ThingSpeak""

Tips:

Download IPwebcam android app on your phone.
Start the web server streaming.
Note down the IP address which is shown in the bottom.

In Takephoto() method:
  Replace the IP address in the url line by the IP address you have noted.

In senddata() method:
  You can choose not to use ThingSpeak by simply commenting the call to this function.
  If you want to use,then change your access key
