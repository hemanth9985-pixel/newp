from openai import OpenAI
from apikey import api_data
import speech_recognition as sr
import pyttsx3
import webbrowser

# Initialize OpenAI
Model = "gpt-4o"
client = OpenAI(api_key=api_data)

def Reply(question):
    try:
        completion = client.chat.completions.create(
            model=Model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Text-to-speech setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # change index for male/female

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Hello, I am ready!")

# Voice input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening .......")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing ....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
        return query.lower()
    except Exception:
        print("Could not understand, please say again.")
        return ""

if __name__ == "__main__":
    while True:
        query = takeCommand()
        if not query:
            continue

        # Handle custom commands first
        if "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")
        elif "bye" in query or "exit" in query or "quit" in query:
            speak("Goodbye!")
            break
        else:
            # Otherwise, use GPT
            ans = Reply(query)
            print(ans)
            speak(ans)







