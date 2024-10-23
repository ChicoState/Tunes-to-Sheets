from pathlib import Path
import essentia.standard as es
import mido
import os
import numpy as np

PPQ = 96 # Pulses per quarter note.
OUTPUT_DIRECTORY = "/public/midi/"
INPUT_DIRECTORY = "/public/audio/"

# Preprocessing improves pitch detection
def preprocess_audio(audio, sample_rate=44100):
    # Apply equal-loudness filter
    equal_loudness = es.EqualLoudness(sampleRate=sample_rate)
    audio_eq = equal_loudness(audio)
    
    # Remove DC offset
    dc_filter = es.DCRemoval(sampleRate=sample_rate)
    audio_dc = dc_filter(audio_eq)
    
    # Apply noise gate to reduce background noise
    noise_gate = es.NoiseGate(sampleRate=sample_rate, threshold=-60)
    audio_clean = noise_gate(audio_dc)
    
    return audio_clean

# Smooth pitch contour and remove low-confidence values
def smooth_pitch_contour(pitch_values, confidence_values, confidence_threshold=0.8):
	# Remove low-confidence pitch values
	pitch_values[confidence_values < confidence_threshold] = 0

	# Apply median filter to remove spurious jumps
	window_size = 5
	pitch_values = np.pad(pitch_values, (window_size//2, window_size//2), mode='edge')
	smoothed_pitch = np.zeros_like(pitch_values)

	for i in range(window_size)(window_size//2, len(pitch_values) - window_size//2):
		window = pitch_values[i-window_size//2:i+window_size//2+1]
		# Consider only 0 values for median
		valid_values = window[window != 0]
		if len(valid_values) > 0:
			smoothed_pitch[i] = np.median(valid_values)
		
	return smoothed_pitch[window_size//2:-window_size//2]

# Returns audio features as ordered tuple (notes, onsets, durations, silence durations)
def extract_audio_features(audiofile: str) -> tuple:
	# Load audio file.
	loader = es.EqloudLoader(filename=audiofile, sampleRate=44100)
	audio = loader()

	#Preprocess audio (preprocessing improves pitch detection)
	audio_clean = preprocess_audio(audio)
	
	# Extract pitch values and confidence.
	pitch_extractor = es.PredominantPitchMelodia(
		frameSize=2048, #inc from 1512 for better freq reso 
		hopSize=128, #dec from 64 for better temporal reso 
		minFrequency=55, # lowest note A1
		maxFrequency=1760, # highest note A6
		minDuration=.1, #dec from 3 secs
		timeContinuity=100, # added for better pitch continuity
		voicingTolerance=0.6 #inc from .2 for better voice dectection
	)
	pitch_values, pitch_confidence = pitch_extractor(audio_clean)

	# Smooth pith contour
	smoothed_pitch = smooth_pitch_contour(pitch_values, pitch_confidence)

	# Segmentation parameters
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