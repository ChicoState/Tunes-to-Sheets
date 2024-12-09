import os
import pathlib as plib
import sys
import pickle
import time

if not os.getcwd().endswith("app") and not os.getcwd().endswith("Audio"):
	raise Exception("Script must be run from /Audio/ or /app/")
sys.path.append(os.getcwd())

import src.models.analyzer as an
import src.models.sheet_generator as sg
import src.controllers.audio_to_sheet as ats
import src.tests.test_data as td


# Freq_to_midi accuracy test
def test1():
	for idx, p in enumerate(td.pitches):
		assert(an.freq_to_midi(p) == td.midi[idx])


# Equal feature lengths
def test2():
	for path in td.audio_paths:
		(file_name, onset_pitches, onset_times, durations) = an.extract_audio_features(path)
		assert(len(onset_pitches) == len(onset_times) == len(durations))


# Valid file names
def test3():
	for path in td.audio_paths:
		(file_name, onset_pitches, onset_times, durations) = an.extract_audio_features(path)
		assert(file_name == plib.Path(path).stem)


# No extraction exceptions
def test4():
	no_exception = True
	try:
		for path in td.audio_paths:
			(file_name, onset_pitches, onset_times, durations) = an.extract_audio_features(path)
	except Exception as e:
		no_exception = False
		
	assert(no_exception == True)


# Generate midi from audio features
def test5():
	if not os.path.exists("src/tests/midi/"):
		os.makedirs("src/tests/midi/")
	for p in td.pickle_paths:
		with open(p, "rb") as f:
			(file_name, onset_pitches, onset_times, durations) = pickle.load(f)
			an.generate_midi_from_audio((file_name, onset_pitches, onset_times, durations), "src/tests/midi/" + file_name + ".mid")
			assert(os.path.exists("src/tests/midi/" + file_name + ".mid") == True)
		for f in os.listdir("src/tests/midi/"):
			os.remove("src/tests/midi/" + f)


# No midi generation exceptions
def test6():
	if not os.path.exists("src/tests/midi/"):
		os.makedirs("src/tests/midi/")
	no_exception = True
	for p in td.pickle_paths:
		with open(p, "rb") as f:
			(file_name, onset_pitches, onset_times, durations) = pickle.load(f)
			try:
				an.generate_midi_from_audio((file_name, onset_pitches, onset_times, durations), "src/tests/midi/" + file_name + ".mid")
			except Exception as e:
				no_exception = False
	for f in os.listdir("src/tests/midi/"):
		os.remove("src/tests/midi/" + f)
	assert(no_exception == True)


# Generate sheet from midi file
def test7():
	if not os.path.exists("src/tests/pdf/"):
		os.makedirs("src/tests/pdf/")
	sg.generate_sheet(td.midi_paths[0], "src/tests/pdf/")
	time.sleep(2)
	assert(os.path.exists("src/tests/pdf/" + plib.Path(td.midi_paths[0]).stem + "-midi.pdf") == True)
	for f in os.listdir("src/tests/pdf/"):
		os.remove("src/tests/pdf/" + f)


# Generate sheet from midi files in under 5 seconds
def test8():
	if not os.path.exists("src/tests/pdf/"):
		os.makedirs("src/tests/pdf/")
	for path in td.midi_paths:
		sg.generate_sheet(path, "src/tests/pdf/")
		time.sleep(2)
		assert(os.path.exists("src/tests/pdf/" + plib.Path(path).stem + "-midi.pdf") == True)
	for f in os.listdir("src/tests/pdf/"):
		os.remove("src/tests/pdf/" + f)
  
# No sheet generation exceptions
def test_9():
	no_exception = True
	if not os.path.exists("src/tests/pdf/"):
		os.makedirs("src/tests/pdf/")
	for path in td.midi_paths:
		try:
			sg.generate_sheet(path, "src/tests/pdf/")
		except Exception as e:
			no_exception = False
	for f in os.listdir("src/tests/pdf/"):
		os.remove("src/tests/pdf/" + f)
	assert(no_exception == True)
 
if __name__ == "__main__":
	test1()
	test2()
	test3()
	test4()
	test5()
	test6()
	test7()
	test8()
 