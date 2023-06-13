FROM python:3.8.8

RUN pip install scipy

RUN pip install pandas

RUN pip install torch

RUN pip install transformers

RUN pip install flask

RUN pip install pymongo

RUN pip install python-decouple

WORKDIR /app

COPY . .

EXPOSE 3000

CMD [ "python", "app.py" ]