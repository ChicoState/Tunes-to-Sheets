from pathlib import Path
import essentia.standard as es
import mido
import os

PPQ = 96 # Pulses per quarter note.
OUTPUT_DIRECTORY = "/public/midi/"
INPUT_DIRECTORY = "/public/audio/"

# Returns audio features as ordered tuple (notes, onsets, durations, silence durations)
def extract_audio_features(audiofile: str) -> tuple:
	# Load audio file.
	loader = es.EqloudLoader(filename=audiofile, sampleRate=44100)
	audio = loader()

	# Extract pitch values and confidence.
	pitch_extractor = es.PredominantPitchMelodia(frameSize=1512, hopSize=64, minDuration=3, voicingTolerance=0.2)
	pitch_values, pitch_confidence = pitch_extractor(audio)
	onsets, durations, notes = es.PitchContourSegmentation(hopSize=50)(pitch_values, audio)

	# Extract rhythm features.
	audio = es.MonoLoader(filename=audiofile, sampleRate=44100)()
	rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
	bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
	tempo = mido.bpm2tempo(bpm) # Microseconds per beat.

	# Compute onsets and offsets for all MIDI notes in ticks.
	offsets = onsets + durations
	silence_durations = list(onsets[1:] - offsets[:-1]) + [0]

	file_name = Path(audiofile).stem
	return (str(file_name), list(notes), list(onsets), list(durations), list(silence_durations), int(tempo))


# Expects a tuple of audio features (notes: list, onsets: list, durations: list, silence durations: list, tempo: list).
def convert_audio_to_midi(audio_features: tuple):
	# Detect errors in audio features tuple.
	match audio_features:
		case (str(file_name), list(notes), list(onsets), list(durations), list(silence_durations), int(tempo)):
			if (len(notes) == len(onsets) == len(durations) == len(silence_durations)):
				pass
			else:
				raise ValueError("Features tuple must all same length")
		case _:
			raise ValueError("Invalid audio features tuple")
		
	file_name, notes, onsets, durations, silence_durations, tempo = audio_features
	
	# Initialize midi file
	mid = mido.MidiFile()
	track = mido.MidiTrack()
	mid.tracks.append(track)
	print("onsets: ", onsets)
	print("durations: ", durations)	

	# Convert features to MIDI data
	for note, onset, duration, silence_duration in zip(list(notes), list(onsets), list(durations), silence_durations): 
		track.append(mido.Message('note_on', note=int(note), velocity=64,
								  time=int(mido.second2tick(onset, PPQ, tempo))))
		track.append(mido.Message('note_off', note=int(note),
								  time=int(mido.second2tick(onset + duration, PPQ, tempo))))

	current_directory = os.getcwd()
	mid.save(current_directory + OUTPUT_DIRECTORY + file_name + ".mid")