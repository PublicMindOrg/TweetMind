# syntax=docker/dockerfile:1

FROM python:3.9.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
