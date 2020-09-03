FROM python:3.8

WORKDIR /buglebot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY buglebot/ .
COPY buglebot.py .

CMD ["python", "./buglebot.py"]
