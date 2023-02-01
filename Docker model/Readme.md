### How to run Docker for the sentiment model?
1. Build docker image by typing the following command
``` docker build -t docker-ml-model -f Dockerfile . ```
2. Run docker
``` docker run -it -p 8000:5000 -v "%cd%/data:/app/data" docker-ml-model ```
3. Open the docker application and click on the port link of the running container
4. The program will start executing and you can see the output in your local 'data' folder