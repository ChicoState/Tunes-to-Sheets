from pathlib import Path
import pretty_midi as pm
import numpy as np
import librosa
import os

PPQ = 96 # Pulses per quarter note.

def freq_to_midi(freq: float) -> int:
	return int(round(12 * (np.log(freq / 220.0) / np.log(2.0)) + 57, 0)) # Treat this as black magic


# Returns audio features as ordered tuple (notes, onsets, durations, silence durations)
def extract_audio_features(absolute_audio_file_path: str) -> tuple:
	y, sr = librosa.load(absolute_audio_file_path)
 
	# Extracting the chroma features and onsets 
	chroma = librosa.stft(y)
	onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
	S = np.abs(chroma)
	pitches, magnitudes = librosa.piptrack(S=S, sr=sr)
	onset_pitches = []
	onset_times = []
	durations	= []

	# Calculate onset times and midi note at that time
	for onset_frame in onset_frames:
		max_index = np.argmax(magnitudes[:, onset_frame])
		pitches_at_onset = pitches[max_index, onset_frame]
		time = librosa.frames_to_time(onset_frame, sr=sr)
		onset_pitches.append(freq_to_midi(pitches_at_onset))
		onset_times.append(time)

	# Compute durations (hacky, just computed as difference to next onset)
	last_onset = onset_times[0]
	for onset_time in onset_times[1:]:
		durations.append(onset_time - last_onset)
		last_onset = onset_time
	last_onset = onset_times[-1]
	durations.append(librosa.get_duration(y=y, sr=sr) - last_onset)
 
	file_name = Path(absolute_audio_file_path).stem
	return (str(file_name), list(onset_pitches), list(onset_times), list(durations))


# Expects a tuple of audio features (notes: list, onsets: list, durations: list, silence durations: list, tempo: list).
def generate_midi_from_audio(audio_features: tuple, absolute_output_directory: str):
	match audio_features:
		case (str(file_name), list(notes), list(onsets), list(durations)):
			if (len(notes) == len(onsets) == len(durations)):
				pass
			else:
				raise ValueError("Features tuple must all same length")
		case _:
			raise ValueError("Invalid audio features tuple")
		
	file_name, notes, onsets, durations = audio_features
 
	midi_mapping = pm.PrettyMIDI()
	inst_program = pm.instrument_name_to_program("Acoustic Grand Piano") # TODO: Find better program instrument in pretty-midi
	instrument = pm.Instrument(program=inst_program, is_drum=False, name='')
	
	# Convert features to MIDI data
	for note, onset, duration in zip(list(notes), list(onsets), list(durations)):
		new_note = pm.Note(velocity=100, pitch=int(note), start=onset, end=onset + duration)
		instrument.notes.append(new_note)
  
	midi_mapping.instruments.append(instrument)
	
	try:	  
		output_dir = absolute_output_directory
		midi_mapping.write(output_dir)
	except Exception as e:
		raise Exception("Error generating MIDI file: " + str(e))