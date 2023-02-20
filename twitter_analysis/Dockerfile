# syntax=docker/dockerfile:1

FROM python:3.9.12

WORKDIR /twitter_analysis

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install -U xgboost

RUN python3 -m pip install scikit-learn

COPY . .

EXPOSE 3000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
