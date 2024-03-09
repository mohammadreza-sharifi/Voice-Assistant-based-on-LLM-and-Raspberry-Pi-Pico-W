from langchain_community.llms import Ollama
import pyttsx3
import speech_recognition as sr


llm = Ollama(model = "phi")
engine = pyttsx3.init()


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
    


while True:
    
    print("speak with me: ")
    
    question = audio_recognizer()
    
    print("your question: ",question)
    
    response = llm.invoke(f"{question} please give me an brief answer.")

    print(response)
    engine.say(response)
    engine.runAndWait()