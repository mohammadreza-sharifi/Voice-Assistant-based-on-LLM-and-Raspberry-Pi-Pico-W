from langchain_community.llms import Ollama
import pyttsx3
import speech_recognition as sr
import pvporcupine 
import pyaudio
import struct
import socket
from playsound import playsound

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify the IP address and port number of your Raspberry Pi Pico W
# You can use the ipconfig or ifconfig command to find out the IP address of your device
ip = '192.168.1.231' # Change this to your Raspberry Pi Pico W IP address
port = 80 # Change this to your Raspberry Pi Pico W port number


llm = Ollama(model = "phi")

engine = pyttsx3.init()

s.connect((ip, port))

def audio_recognizer():
    speech = sr.Recognizer()
    
    with sr.Microphone() as source:
        
        audio = speech.listen(source)
        
        text = ''
        
        try:
            text = speech.recognize_google(audio,language = "en-US")
            #print(text)
            
        except:
            print("I can't hear you.....")
            
    return text

# Create a Porcupine instance with your custom wake word
handle = pvporcupine.create(
    access_key='YNkeq9KAoy5Q2pQaf6Ufo9IFf5fNXR9kgThOx/KMpu2nAizLCRQVsw==', # Get this from Picovoice Console
    keyword_paths=['D:\\getting started with LLMs\\hey-pico_en_windows_v3_0_0.ppn']) # Download this from Picovoice Console

# Get the required audio input parameters
pa = pyaudio.PyAudio()
sample_rate = handle.sample_rate
frame_length = handle.frame_length
audio_stream = pa.open(
    rate=sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=frame_length)


while True:
    
    #print("speak with me: ")
    
    # Read one frame of audio
    pcm = audio_stream.read(frame_length)
    pcm = struct.unpack_from("h" * frame_length, pcm)

    # Pass the audio frame to Porcupine
    keyword_index = handle.process(pcm)

    # Check if a wake word is detected
    if keyword_index >= 0:
        
        engine.say("i am at your service........")
        engine.runAndWait()
        
        print("ask me a question: ")
        
        # Wake word detected, listen for the question
        question = audio_recognizer()
    
        print("your question: ",question)
        
        if question == "turn on the light":
            cmd = 'o'            
            cmd = cmd.encode()
            s.send(cmd)
            
            engine.say("light is on")
            engine.runAndWait()
            
        elif question == "turn off the light":            
            cmd = 'f'
            cmd = cmd.encode()
            s.send(cmd)
            
            engine.say("light is off")
            engine.runAndWait()
            
        elif question == "play a song":
            song = "D:\\voice assistant based on llms and rpi pico w\\['1'].wav"
            playsound(song)
            
        elif question == "what is the temp":
            cmd = "temp"
            cmd = cmd.encode()
            s.send(cmd)
            response = s.recv(1024)
            
            temp = float(response.decode())
            
            print(temp)
            engine.say(f"temperature is {temp} degree Celsius")
            engine.runAndWait()

        elif question == "what is the humidity":
            cmd = "humidity"
            cmd = cmd.encode()
            s.send(cmd)
            response = s.recv(1024)
            
            hum = float(response.decode())
            
            print(hum)
            engine.say(f"humidity is {hum} percent")
            engine.runAndWait()
                      
        else:
            response = llm.invoke(f"{question}, please give me a brief answer.")

            print(response)
            engine.say(response)
            engine.runAndWait()
