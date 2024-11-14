import subprocess
import os
from pathlib import Path

OUTPUT_DIRECTORY = "public/pdf/"
INPUT_DIRECTORY = "public/midi/"

def generate_sheet(absolute_midi_file_path: str, absolute_output_directory: str) -> bool:
    try:
        midi_file_path = Path(absolute_midi_file_path)
        output_file_path = Path(absolute_output_directory)
       
        # Generate PDF
        subprocess.run(["midi2ly", midi_file_path.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  check=True, cwd=midi_file_path.parent)
        subprocess.run(["lilypond", midi_file_path.name.replace(".mid", "-midi.ly")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  check=True, cwd=midi_file_path.parent)
        
        # Move pdf to output directory
        subprocess.run(["cp", str(midi_file_path.absolute()).replace(".mid", "-midi.pdf"), output_file_path.absolute()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  check=True, cwd=midi_file_path.parent)
        
        # Cleanup junk files
        subprocess.run(["rm", midi_file_path.name.replace(".mid", "-midi.midi")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  check=True, cwd=midi_file_path.parent)
        subprocess.run(["rm", midi_file_path.name.replace(".mid", "-midi.ly")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  check=True, cwd=midi_file_path.parent)
        subprocess.run(["rm", midi_file_path.name.replace(".mid", "-midi.pdf")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  check=True, cwd=midi_file_path.parent)
    except Exception as e:
        raise Exception("Error generating PDF: " + str(e))