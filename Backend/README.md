Running using Docker
1. Have Docker Desktop running in background
2. Make sure Dockerfile and requirements.txt are in current directory
3. To run you can either do container or image:
   Container:
   1. docker compose up --build [To run]
   2. Go to http://localhost:8000 To see program
   3. Ctrl + C to stop running
   Image:
   1. docker build -t fileservice .
   2. docker run --rm -p 8000:8000 fileservice 
   3. Ctrl + C to stop running
   4. To remove the docker image after done use: docker rmi fileservice
