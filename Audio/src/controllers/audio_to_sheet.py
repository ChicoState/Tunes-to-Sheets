import sys
import os
from pathlib import Path
import src.models.analyzer as an
import src.models.sheet_generator as sg

AUDIO_DIRECTORY = "/public/audio/"
MIDI_DIRECTORY = "/public/midi/"
PDF_DIRECTORY = "/public/pdf/"

def generate_sheet_from_audio(audio_file_name: str):
	audio_path = Path(os.getcwd() + AUDIO_DIRECTORY + audio_file_name)
	midi_path = Path(os.getcwd() + MIDI_DIRECTORY + audio_path.stem + ".mid")
	pdf_path = Path(os.getcwd() + PDF_DIRECTORY + audio_path.stem + ".pdf")
	
	if not os.path.exists(audio_path.absolute()):
		raise FileNotFoundError("Could not file file: " + audio_file_name)

	if not os.path.exists(audio_path.parent.absolute()):
		os.makedirs(audio_path.parent.absolute())
	if not os.path.exists(midi_path.parent.absolute()):
		os.makedirs(midi_path.parent.absolute())
	if not os.path.exists(pdf_path.parent.absolute()):
		os.makedirs(pdf_path.parent.absolute())
	
	an.generate_midi_from_audio(an.extract_audio_features(str(audio_path.absolute())), str(midi_path.absolute()))
	#sg.generate_sheet(str(midi_path.absolute()), str(pdf_path.absolute()))

generate_sheet_from_audio("testfile.mp3")