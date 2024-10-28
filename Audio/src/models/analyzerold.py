from pathlib import Path
import essentia.standard as es
import pretty_midi as pm
import os

PPQ = 96 # Pulses per quarter note.
OUTPUT_DIRECTORY = "/Audio/public/midi/"
INPUT_DIRECTORY = "/Audio/public/audio/"

# Returns audio features as ordered tuple (notes, onsets, durations, silence durations)
def extract_audio_features(audiofile: str) -> tuple:
	# Load audio file.
	loader = es.EqloudLoader(filename=audiofile, sampleRate=44100)
	audio = loader()

	# Extract pitch values and confidence.
	pitch_extractor = es.PredominantPitchMelodia(frameSize=1512, hopSize=64, minDuration=3, voicingTolerance=0.2)
	pitch_values, pitch_confidence = pitch_extractor(audio)
	onsets, durations, notes = es.PitchContourSegmentation(hopSize=50)(pitch_values, audio)

	file_name = Path(audiofile).stem
	return (str(file_name), list(notes), list(onsets), list(durations))


# Expects a tuple of audio features (notes: list, onsets: list, durations: list, silence durations: list, tempo: list).
def convert_audio_to_midi(audio_features: tuple):
	# Detect errors in audio features tuple.
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
	inst_program = pm.instrument_name_to_program("Cello") # TODO: Find better program instrument in pretty-midi
	instrument = pm.Instrument(program=inst_program, is_drum=False, name='Cello')
	
	
	# Convert features to MIDI data
	for note, onset, duration in zip(list(notes), list(onsets), list(durations)): 
		new_note = pm.Note(velocity=100, pitch=int(note), start=onset, end=onset+duration)
		instrument.notes.append(new_note)
  
	midi_mapping.instruments.append(instrument)
	
	current_directory = os.getcwd()
 
	output_dir = current_directory + OUTPUT_DIRECTORY + file_name + ".mid"
	midi_mapping.write(output_dir)
	
	
a_file = "/home/koris/Tunes-to-Sheets/Audio/public/audio/testfile.mp3"
features = extract_audio_features(a_file)
convert_audio_to_midi(features)