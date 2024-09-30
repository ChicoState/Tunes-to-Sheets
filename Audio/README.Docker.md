### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)

### Installing new python modules
1. First ensure you have virtualenv installed
- pip install virtualenv
2. cd in AudioProcessor folder
3. Create env
- python3 -m venv .env
4. activate env
- source .env/bin/activate
5. install requirements
- pip install -r requirements.txt
6. install new module(s)
- pip install ....
7. add new module to requirements
- pip freeze > requirements.txt