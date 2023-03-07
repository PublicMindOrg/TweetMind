### How to run Docker for the sentiment model?
1. Download model folders from shared drive and save it in a local folder
2. Clone files from 'Docker model' in the same folder
3. Build docker by running the following command
``` docker build -t docker-ml-model -f Dockerfile . ```
4. Run docker with the command 
``` docker run -it -p 8000:5000 -v "%cd%/data:/app/data" docker-ml-model ```
5. Open docker application and click on the 8000:5000 port link (will open localhost) of the running container
6. The program will start executing. You can see the output in your local 'data' folder when the localhost page returns a "Done" message