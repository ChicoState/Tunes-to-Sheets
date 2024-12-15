#File Service Backend
#Import the necessary libraries of fastapi, file import
from fastapi import FastAPI, File, UploadFile, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
#Library for the communication between ports
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import shutil
import sys
from typing import List

#Activates instance and set up format using FastAPI
app = FastAPI()

#Create path to put output files in Backend Directory[dirname gets parent followed by path]
AUDIO_DIRECTORY = os.path.join(os.path.dirname(os.getcwd()), "Audio", "public", "audio")
if not os.path.exists(AUDIO_DIRECTORY):
    os.makedirs(AUDIO_DIRECTORY)  #Create the directory if it doesn't exist
#CORS middle ware since running on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173",],  #port related that accepts requests and posts
    allow_credentials=True,# * allows all 
    allow_methods=["*"],
    allow_headers=["*"],
)

#Handling multiple file upload
@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []#Array for multiple files
    max_size = 10 * 1024 * 1024  # 10MB limit
    allowed_types = ['audio/mpeg','audio/mp4', 'audio/wav', 'audio/midi']  #mpeg/MP3, MP4(audio only), WAV, and MIDI files allowed

    try:
        for file in files:
            #FileTypes allowed [Unit testing] 
            if file.content_type not in allowed_types:
                raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Only MP3, WAV, and MIDI files are allowed.")

            #File Size[Unit testing]
            if file.size > max_size:
                raise HTTPException(status_code=400, detail=f"File is too large: {file.filename}. Max file size is 10MB.")

            #Save the file to directory so it can be converted
            upload_path = os.path.join(AUDIO_DIRECTORY, file.filename)
            with open(upload_path, "wb") as f:
                content = await file.read()
                f.write(content)
            filenames.append(file.filename)
        #Send first file name 
        return {"filename": filenames[0], "message": "Files uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

