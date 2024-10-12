#File Service Backend part CSCI 430
#Carlos Flores Rivera
from typing import Annotated
#Import the necessary libraries of fastapi, file import
from fastapi import FastAPI, File, UploadFile, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates #Template library for HTML portion
from fastapi.staticfiles import StaticFiles #Static Files [need a static directory]
#File processing
from pydub import AudioSegment 
import os
from tempfile import NamedTemporaryFile #Used to create temporary files
#AudiotoSheet generator [In progress]
import librosa
import numpy as np
from music21 import stream, note, meter, key

#Create path to put output files
output_path = os.path.join(os.getcwd(), "output_directory")
if not os.path.exists(output_path):
    os.makedirs(output_path)  #Create the directory if it doesn't exist

#Activates instance and set up format using FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")#Set up Jinja2 templates [for bootstrap template]
#Mount static files for JavaScript and CSS (if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

#Homepage with upload form using the template of Jinja2 [HOW IT LOOKS]
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request}) #Uses the template from upload.html

#Converting the mp3 file to wav
def MP3_to_WAV(mp3_file, wav_file_name):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file_name, format="wav")
    return wav_file_name

#Handling file upload [ACTION CREATED WHEN PRESSED]
@app.post("/uploadfile/")
async def upload_file(request: Request, file: UploadFile = File(...)):#Specify the form data, body of file
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3: #use a temp file to hold upload
        temp_mp3.write(await file.read())
        temp_mp3_path = temp_mp3.name
    wav_file_name = os.path.join(output_path, f"{os.path.basename(temp_mp3_path).replace('.mp3', '.wav')}")#Changes the formate of the temp_file
    wav_file_path = MP3_to_WAV(temp_mp3_path, wav_file_name)#Call function for conversion
    # After exporting the WAV file check if converted right [Error checking]
    if os.path.exists(wav_file_path):
        print(f"WAV file created successfully at: {wav_file_path}")
        return templates.TemplateResponse("upload.html", {
            "request": request, 
            "filename": os.path.basename(wav_file_path),
        })
    raise HTTPException(status_code=400, detail="File conversion failed.")

#Add download option to download a file on webpage[Currently works with WAV]
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(output_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='audio/wav', filename=os.path.basename(file_path))
    else:
        raise HTTPException(status_code=404, detail="File not found")
