# [Software] Magtility
Magtility is a WIP utility for decoding raw magstripe swipes saved as a .wav file into binary data.

<img width="1036" alt="Screen Shot 2022-03-13 at 5 51 43 PM" src="https://user-images.githubusercontent.com/17792367/158081002-bec4dde1-7b28-4035-8050-f1dabe079472.png">

<img width="992" alt="Screen Shot 2022-03-13 at 5 51 57 PM" src="https://user-images.githubusercontent.com/17792367/158081007-9b40b44b-b7bf-4083-8745-1877e91bea6c.png">

<img width="960" alt="Screen Shot 2022-03-13 at 5 52 31 PM" src="https://user-images.githubusercontent.com/17792367/158081008-a086e156-5174-44c8-bd4b-1d0d51116b00.png">

### How to use:
1. Using a program like Audacity, record a swipe from the card using a magnetic head plugged into the mic port of your computer.
2. In Magtility, click "Select File" and select the file you want to decode.
3. Select the magnetic track number of the recording (or multiple if the recorded track spans multiple tracks).
4. Click "Load File" and the binary data will show up in the "Raw Binary" section under the specified track.
5. Further data (such as flux timings and sample peaks) can be viewed using the "Display Data" button.

### Hardware Required:
For this program, a special magstripe reader is needed. It needs to be a reader that has its magnetic head directly connected to an aux jack that can be plugged into the microphone input of your computer. Old Square credit card readers are one such example (new Square credit card readers can be used aswell but require some modification to bypass the encryption circuitry). A reader can also be made from soldering an aux jack onto any suitable magnetic read head (such as from a tape cassette player).
