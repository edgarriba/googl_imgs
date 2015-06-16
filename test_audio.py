import speech_recognition as sr
from googl_down import search

r = sr.Recognizer(language='en-US')
r.energy_threshold = 4000

while True:

	with sr.Microphone() as source:                # use the default microphone as the audio source
		audio = r.adjust_for_ambient_noise(source, duration = 1) # listen for 1 second to calibrate the energy threshold for ambient noise levels
		audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

	try:

		rec_term = str(r.recognize(audio))

		if 'search' in rec_term:
		  
		  # search the word
		  searchTerm = rec_term.replace('search ', '')
		  print 'Searching: %s' % searchTerm

		  search( searchTerm )

		else:
			print 'You said: %s' % rec_term    # recognize speech using Google Speech Recognition


	except LookupError:                            # speech is unintelligible
	  print("Could not understand audio")

