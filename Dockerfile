FROM python:3.9.5-slim

RUN apt-get update && apt-get install -y libpq-dev gcc 

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit","run","app.py","--server.port=8501", "--server.address=0.0.0.0"]
