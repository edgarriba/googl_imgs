import speech_recognition as sr
from googl_down import search

r = sr.Recognizer()
r.energy_threshold = 4000

with sr.Microphone() as source:                # use the default microphone as the audio source
	audio = r.adjust_for_ambient_noise(source, duration = 1) # listen for 1 second to calibrate the energy threshold for ambient noise levels
	audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

try:
  print("You said: " + r.recognize(audio))    # recognize speech using Google Speech Recognition
  
  # search the word
  searchTerm = str(r.recognize(audio))
  search( searchTerm )

except LookupError:                            # speech is unintelligible
  print("Could not understand audio")

