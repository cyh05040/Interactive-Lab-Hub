# You're a wizard, Yen-Hao

<img src="https://pbs.twimg.com/media/Cen7qkHWIAAdKsB.jpg" height="400">

In this lab, we want you to practice wizarding an interactive device as discussed in class. We will focus on audio as the main modality for interaction but there is no reason these general techniques can't extend to video, haptics or other interactive mechanisms. In fact, you are welcome to add those to your project if they enhance your design.


## Text to Speech and Speech to Text

In the home directory of your Pi there is a folder called `text2speech` containing some shell scripts.

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav

```

you can run these examples by typing 
`./espeakdeom.sh`. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts

```

You can also play audio files directly with `aplay filename`.

After looking through this folder do the same for the `speech2text` folder. In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

## Serving Pages

In Lab 1 we served a webpage with flask. In this lab you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/$ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to [http://ixe00.local:5000]()


## Demo

In the [demo directory](./demo), you will find an example wizard of oz project you may use as a template. **You do not have to** feel free to get creative. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You can control what system says from the controller as well.

## Optional

There is an included [dspeech](./dspeech) demo that uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) for speech to text. If you're interested in trying it out we suggest you create a seperarate virutalenv. 



# Lab 3 Part 2

Create a system that runs on the Raspberry Pi that takes in one or more sensors and requires participants to speak to it. Document how the system works and include videos of both the system and the controller.

## Prep for Part 2

1. Sketch ideas for what you'll work on in lab on Wednesday.

![SmartyPi Toilet](IMG_1366.jpg)

## Share your idea sketches with Zoom Room mates and get feedback

Justin Liu:   
I think the idea is brilliant, especially the part how you envision toilet as a robot. I love how you incorporate the weighing function onto the toilet, which can replace a scale in your bathroom. I would be interested to see if it's possible to measure more data such as your body fat or metabolism.    
    
Ming-Chun Lu:   
Very nice idea! I would buy one in my bathroom. I wish there is a heating and cooling feature for you can install and ask the toilet to change the tempurature through voice. 


## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*    
The device, I called it SmartyPi Toilet. It has several feature, which is quite similar to having a smart home speaker within a toilet. For example, it can order more toilet papers when you are out and also play some music during the process to make the user feel better.   
Furthermore, it has a couple advanced feature that home speakers aren't able to do such as flushing the toilet with voice and mearue user's weight when they are sitting on the toilet. It has a scale sensor within the toilet seat and it will record your weight into the Rasberry Pi. Every time the user, ask to have his or her weight measured, SpartyPi toilet would inform the user that if he or she has gained weight or lost weight. 


*Include videos or screencaptures of both the system and the controller.*    


![SmartyPi Toilet](whole.jpg)  
![SmartyPi Toilet](side.jpg)  
![SmartyPi Toilet](close.jpg)  
![SmartyPi Toilet](Photo_measure+weight.jpg)  


       
[Open Toilet Failure](https://youtu.be/Rh7ZgXMFY70)    
[Open and Close Toilet Success](https://youtu.be/Wlf6470p3YE)    
[Order Toilet Paper and Play Music](https://youtu.be/Dq5ogA1W3oU)    
[Measure User Weight](https://youtu.be/kOcGTPgqF98)     


## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)
    
Two people tested the system - Ming-Chun (Jeff) Lu, Justin Liu.  




Answer the following:

### What worked well about the system and what didn't?   
The open and close feature of the smarty pi toilet worked very well. The users really like how the toilet open in time and closed it in a smooth motion. They appreciate how the toilet seat doesn't just slams down, which makes the device looks even smarter.    
The measure weight feature doesn't work as well as imagined. It is mainly due to people got long legs and it would be too difficult to measure the user's weight correctly while having their feet touching the floor. This would be something I cant think about and possibly redesign.   

### What worked well about the controller and what didn't?

The controller works very well and is easy to use with  no obvious latency.   

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?    

The react time of the device would decide a big part of the user experience and the time latency can be a problem. It is imperative for the user to see the according reaction within two seconds, anything above that would be a little confusing for the user. Also, only limited action can be conducted, for example it can only do one action at once. Last but not least, smarty pi toilet actions can only be conducted in a quiet place without too much noise.   
   

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?   

For the open and close seat function: It would be very interesting if the user could adjust the seat opening and closing speed according to his or her preference.   
For the play music function: It would be more user friendly could sense the volume and give him or her the option to adjust accordingly. Furthermore, it can detect the current noise level in the room and decide on the volume of music accordingly.   
For the weight measuring feature: It will help the user to keep track of his or her weight and compare with the previous data and provide user the trend of the weight. (If it's getting heavier/ lighter by what percentage.)


