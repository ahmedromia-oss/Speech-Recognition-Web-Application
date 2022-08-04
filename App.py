
# from multiprocessing.sharedctypes import Value
import flask
import os
from gtts import gTTS
import speech_recognition as sr # recognize speech

from gtts import gTTS # google text to speech
import random
from time import ctime
from sqlalchemy import false # get time details

import yfinance as yf # to fetch financial data

app = flask.Flask(__name__) #to start application

def speak(mytext):
    output = gTTS(text=mytext , lang = 'en' , slow=false)
    output.save("output.mp3")
    os.system("start output.mp3")
@app.route("/" , methods = ["get" , "post"])

def index():

    Mytext = "Press on the mic to record"    

    if flask.request.method == "Post":
        

            
        return flask.redirect(flask.url_for("Record"))
    
    return flask.render_template("index.html" , value = Mytext)
  

@app.route('/Record' , methods=["get" , "post"])

def Record():
    
    r = sr.Recognizer() # initialise a recogniser

    Mytext = "Press on the mic to record"    

    with sr.Microphone() as source: # microphone as source

            print("Listening......")
            audio = r.listen(source)

            try:
                

                query = r.recognize_google(audio, language='en-in') # take the audio to the nearest posible text
            
                if ("search for") in query and 'youtube' not in query:
                        search_term = query.split("for")[-1]

                        url = f"https://google.com/search?q={search_term}"
                        # ["search for" , "smartest man "]
                        speak(f"searching for {search_term} on google")


                        return flask.redirect(url)
                if ("find") in query and 'YouTube' in query:

                    search_term = query.split("find")[-1]

                    url = f"https://www.youtube.com/results?search_query={search_term}"
                    speak(f"searching for {search_term} on youtube")
                
                    return flask.redirect(url)
               
                
                   

                
                if ("my name is") in query:

                    person_name = query.split("is")[-1].strip()

                    query = f"okay, i will remember that {person_name}"
                    speak(query)
                    
            # 3: greeting
                if ("how are you") in query or ("how are you doing") in query :

                    query = (f"I'm very well, thanks for asking")
                    speak(query)

            # 4: time
                if ("what's the time") in query or ("what time is it") in query :

                    time = ctime().split(" ")[3].split(":")[0:2]
                    if time[0] == "00":

                        hours = '12'
                    else:

                        hours = time[0]

                        minutes = time[1]

                        time = f'{hours} : {minutes}'

                        query = time
                        speak(query)

                return flask.render_template( "Record.html" ,value = query)

            except Exception:
                speak("Did not catch")
                return flask.render_template( "Record.html" ,value = "did not catch that")



if __name__ == "__main__":

    app.run(debug = True)